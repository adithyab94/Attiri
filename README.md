<p align="center" width="100%">
<a href="https://adithyabalaji.notion.site/Attiri-A-LLaMa-Model-for-Tamil-d49b91e2d7704c3286fd4ac4c1934c18" target="_blank"><img src="assets/attiri_logo.png" alt="Stanford-Alpaca" style="width: 50%; min-width: 300px; display: block; margin: auto;"></a>
</p>

<h1 align="center">
  <br />
  Attiri: Dataset and a LLaMa based instruction-following large language model for Tamil
</h1>

<div align="center">

  <a href="">![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)</a>
  <a href="">![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)</a>
  <a href="">![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)</a>

</div>

Attiri, an extension of the LLaMa, aims to build and share an instruction-following LLaMA model for the Tamil language. Our project includes the similar 52K data used for fine-tuning the original model but in Tamil language, as well as the code for generating the data and fine-tuning the model. As of now, the project is under development and will be available soon.

The repository contains

- Dataset
- Code to generate the data
- TODO: Code to fine tune LLaMA 7B and possible the the models including PaLM

## Table of Contents

1. [Preparation](#preparation)
   1. [Setup](#setup)
   2. [Dataset](#dataset)
2. [Usage](#usage)
3. [TODO](#to-do)
4. [Citation](#citation)
5. [To Contribute](#to-contribute)
6. [Acknowledgments](#acknowledgments)
7. [License](#license)
8. [Fun-Fact](#fun-fact)

## Preparation

### Setup

To use the program, you must have Python 3.9+ (recommended = 3.9) and the necessary packages installed. You can install the necessary packages using pip:

Create a new Conda environment with Python 3.9:

```bash
conda create --name attiri python=3.9
```

Activate the new environment:

```bash
conda activate attiri
```

```bash
pip install -r requirements.txt
```

### Dataset

| S.No | Dataset | Description | Count | I/O    |
|------|---------|-------------|-------|--------|
| 1    | [Attiri-Alpaca](data/attiri_alpaca_data.json)  | Tamil version of the Stanford Alpaca dataset | 52K| Instruction, Input, Output|
| 2    | [Attiri-Nomic](https://drive.google.com/drive/folders/1_uNWzjNJ8R-57Rd6N-ybYisDf6Ig8-eG?usp=share_link)  | Tamil version of the Nomic AI GPT4ALL dataset | 500K | Prompt, Response|
| 3    | [IndicCorp](https://ai4bharat.iitm.ac.in/corpora)| A single large text file containing one sentence per line. The publicly released version is randomly shuffled, untokenized and deduplicated. | 31.5M| Sentences|

``attiri_data.py`` translates instruction data for the Alpaca dataset from one language to another using the Google Translate API. The program is built with Click and tqdm for command-line argument parsing and progress tracking, respectively.

Attiri Nomic data is available on request, including a csv file with the prompt and response in English and their corresponding tamil translations. To Request : [Click Here](https://drive.google.com/drive/folders/1_uNWzjNJ8R-57Rd6N-ybYisDf6Ig8-eG?usp=share_link)

## Usage

Here are some examples of how to use the program:

Translate data from alpaca_data.json in English to French and save it to output.json:

```bash
python attiri_data.py -s en -t fr -d alpaca alpaca_data.json output.json
```

Note that the program may take some time to run, especially for large input files or when translating to many different languages.

## To-Do

- [X] Translate alpaca json data into Tamil
- [X] Translate nomic json data into Tamil
- [ ] Clean training data
- [ ] Finetuning with lora uing Local GPU
- [ ] Release vBeta model
- [ ] Output model to hugging face
- [ ] Demo UI (Hugging Face / Hosted app)
- [ ] Finetuning with lora using Cloud GPU (8x A100s)
- [ ] Release v1.0 model
- [ ] Output model to hugging face
- [ ] Demo UI (Hugging Face / Hosted app)

## Citation

Please cite this project if you use the dataset, model or code in this repo. (Note: Naturally you should also cite the original LLaMA, Stanford Alpaca, and LoRa papers)

```BibTeX
@misc{Attiri,
  author = {Adithya Balaji},
  title = {Attiri: Dataset and a LLaMa based instruction-following large language model for Tamil},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/adithyab94/Attiri}},
}
```

## To Contribute

This project is actively looking for collaborators. If you are interested in contributing to this project, please raise a pull request or [write to me](mailto:adithya.b94@gmail.com)

## Acknowledgments

Thanks for the open source projects - [LLaMA](https://github.com/facebookresearch/llama), [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca), and [Alpaca-Lora](https://github.com/tloen/alpaca-lora) from which this project is inspired.

Thanks to the [AI4Bharat](https://ai4bharat.iitm.ac.in/) team for the [IndicCorp](https://ai4bharat.iitm.ac.in/corpora) dataset.
and [Nomic](https://github.com/nomic-ai/gpt4all) for the  GPT4ALL dataset.  

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Fun-Fact

The word "Attiri" (["அத்திரி"](https://agarathi.com/word/%E0%AE%85%E0%AE%A4%E0%AF%8D%E0%AE%A4%E0%AE%BF%E0%AE%B0%E0%AE%BF)) is used by the poet Ilango in the famous Tamil epic Silappadikaram which acccording to the Tamil dictionary could be a camel, a distant relative of the Llamas and Alpacas.

  வான வண்கையன் அத்திரி ஏற\
  மான் அமர் நோக்கியும் வையம் ஏறிக்\
  கோடி பல அடுக்கிய கொழிநிதிக் குப்பை..\
  \
  *- கடலாடு காதை, சிலப்பதிகாரம்*
