###-----------------------------
# Module to finetune the model #
###-------------------------------
from peft import (
    LoraConfig,
    get_peft_model,
    get_peft_model_state_dict,
    prepare_model_for_int8_training,
)
from transformers import LlamaTokenizer, LlamaForCausalLM
from datasets import load_dataset

import transformers
import torch
import json


class LlamaTrainer:
    def __init__(self, base_model_path, data_file_path):
        self.base_model_path = base_model_path
        self.data_file_path = data_file_path

        self.model = None
        self.tokenizer = None
        self.train_data = None
        self.val_data = None
        self.trainer = None
        self.BASE_MODEL = self.base_model_path

        self.prepare_data()
        self.prepare_params()
        self.prepare_model()
        self.prepare_trainer()

    def prepare_params(self):
        with open("parameters.json", "r") as f:
            params = json.load(f)

        self.CUTOFF_LEN = params["CUTOFF_LEN"]
        self.LORA_R = params["LORA_R"]
        self.LORA_ALPHA = params["LORA_ALPHA"]
        self.LORA_DROPOUT = params["LORA_DROPOUT"]
        self.LORA_TARGET_MODULES = params["LORA_TARGET_MODULES"]
        self.BATCH_SIZE = params["BATCH_SIZE"]
        self.MICRO_BATCH_SIZE = params["MICRO_BATCH_SIZE"]
        self.GRADIENT_ACCUMULATION_STEPS = self.BATCH_SIZE // self.MICRO_BATCH_SIZE
        self.LEARNING_RATE = params["LEARNING_RATE"]
        self.TRAIN_STEPS = params["TRAIN_STEPS"]
        self.OUTPUT_DIR = params["OUTPUT_DIR"]

    def prepare_data(self):
        data = load_dataset("json", data_files=self.data_file_path)
        train_val = data["train"].train_test_split(test_size=200, shuffle=True, seed=42)
        self.train_data = train_val["train"].map(self.generate_and_tokenize_prompt)
        self.val_data = train_val["test"].map(self.generate_and_tokenize_prompt)

    def prepare_model(self):
        self.model = LlamaForCausalLM.from_pretrained(
            self.BASE_MODEL,
            load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        self.tokenizer = LlamaTokenizer.from_pretrained(self.BASE_MODEL)
        self.tokenizer.pad_token_id = (
            0  # unk. we want this to be different from the eos token
        )
        self.tokenizer.padding_side = "left"

        self.model = prepare_model_for_int8_training(self.model)
        config = LoraConfig(
            r=self.LORA_R,
            lora_alpha=self.LORA_ALPHA,
            target_modules=self.LORA_TARGET_MODULES,
            lora_dropout=self.LORA_DROPOUT,
            bias="none",
            task_type="CAUSAL_LM",
        )
        self.model = get_peft_model(self.model, config)
        self.model.print_trainable_parameters()

    def prepare_trainer(self):
        self.training_arguments = transformers.TrainingArguments(
            per_device_train_batch_size=self.MICRO_BATCH_SIZE,
            gradient_accumulation_steps=self.GRADIENT_ACCUMULATION_STEPS,
            warmup_steps=100,
            max_steps=self.TRAIN_STEPS,
            learning_rate=self.LEARNING_RATE,
            fp16=True,
            logging_steps=10,
            optim="adamw_torch",
            evaluation_strategy="steps",
            save_strategy="steps",
            eval_steps=50,
            save_steps=50,
            output_dir=self.OUTPUT_DIR,
            save_total_limit=3,
            load_best_model_at_end=True,
            report_to="tensorboard",
        )

    def train(self):
        self.trainer = transformers.Trainer(
            model=self.model,
            train_dataset=self.train_data,
            eval_dataset=self.val_data,
            args=self.training_arguments,
            data_collator=transformers.DataCollatorForSeq2Seq(
                self.tokenizer, pad_to_multiple_of=8, return_tensors="pt", padding=True
            ),
        )
        self.model.config.use_cache = False
        old_state_dict = self.model.state_dict
        self.model.state_dict = (
            lambda self, *_, **__: get_peft_model_state_dict(self, old_state_dict())
        ).__get__(self.model, type(self.model))

        self.model = torch.compile(self.model)

        self.trainer.train()
        self.model.save_pretrained(self.OUTPUT_DIR)
