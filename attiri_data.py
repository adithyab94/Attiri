from deep_translator import GoogleTranslator
from typing import Dict, List
from tqdm import tqdm

import pandas as pd

import click
import json


class AlpacaDataProcessor:
    def __init__(self, filename: str) -> None:
        """
        :param filename: The name of the file to be loaded

        Initialize the class with the filename
        """
        self.filename = filename
        self.data = None

    def load(self) -> None:
        """
        :return: None

        Load the data from the file
        """
        with open(self.filename, "r") as f:
            self.data_raw = json.load(f)
            self.data = {ind: item for ind, item in enumerate(self.data_raw)}

    def get_translated_dict_list(self, source, target) -> List:
        """
        :return: List

        Return the translated data
        """
        self.translated_list = [data for data in self.translate(source, target)]

    def save(self, filename: str) -> None:
        """
        :param filename: The name of the file to be saved
        :return: None

        Save the data to the file
        """
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(self.translated_list, file, ensure_ascii=False)

    def translate(self, source: str, target: str) -> None:
        """
        :param source: The source language
        :param target: The target language
        :return: None

        Translate the data from the source language to the target language
        """
        my_translator = GoogleTranslator(source=source, target=target)
        for key in tqdm(self.data.keys()):
            translated_data = {}
            data = self.data[key]
            for value in data.values():
                if "code" in value or "program" in value:
                    pass
                else:
                    translated_data["instruction"] = my_translator.translate(
                        text=data["instruction"]
                    )
                    if data["input"].isnumeric():
                        translated_data["input"] = data["input"]
                    else:
                        translated_data["input"] = my_translator.translate(
                            text=data["input"]
                        )
                    if data["output"].isnumeric():
                        translated_data["output"] = data["output"]
                    else:
                        translated_data["output"] = my_translator.translate(
                            text=data["output"]
                        )
            yield translated_data


class NomicDataProcessor:
    def __init__(self, filename: str) -> None:
        """
        :param filename: The name of the file to be loaded

        Initialize the class with the filename
        """
        self.filename = filename
        self.data = None

    def load(self) -> None:
        """
        :return: None

        Load the data from the file
        """

        # load jsonl file as dictionary

        with open(self.filename, "r") as f:
            self.data_raw = pd.read_csv(f)
            self.data = self.data_raw.T.to_dict()

    def get_translated_dict_list(self, source, target) -> List:
        """
        :return: List

        Return the translated data
        """
        self.translated_list = [data for data in self.translate(source, target)]

    def save(self, filename: str) -> None:
        """
        :param filename: The name of the file to be saved
        :return: None
        """
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(self.translated_list, file, ensure_ascii=False)

    def translate(self, source: str, target: str) -> None:
        my_translator = GoogleTranslator(source=source, target=target)
        for key in tqdm(self.data.keys()):
            translated_data = {}
            data = self.data[key]
            for value in data.values():
                if "code" in value or "program" in value:
                    pass
                else:
                    if data["prompt"].isnumeric():
                        translated_data["prompt"] = data["prompt"]
                    else:
                        translated_data["prompt"] = my_translator.translate(
                            text=data["prompt"]
                        )
                    if data["response"].isnumeric():
                        translated_data["response"] = data["response"]
                    else:
                        translated_data["response"] = my_translator.translate(
                            text=data["response"]
                        )
            yield translated_data


@click.command()
@click.option("--source", "-s", default="auto", help="Source language (default: auto)")
@click.option("--target", "-t", required=True, help="Target language")
@click.option(
    "--dataset",
    "-d",
    required=True,
    help="Dataset to be translated (alpaca or nomic)",
    type=click.Choice(["alpaca", "nomic"]),
)
@click.argument("--input_file", "-i", type=click.Path(exists=True))
@click.argument("--output_file", "-o", type=click.Path())
def main(
    source: str, target: str, dataset: str, input_file: str, output_file: str
) -> None:
    if dataset == "alpaca":
        data = AlpacaDataProcessor(input_file)
    elif dataset == "nomic":
        data = NomicDataProcessor(input_file)
    data.load()
    try:
        data.get_translated_dict_list(source=source, target=target)
    except Exception as e:
        ValueError(e)
    data.save(output_file)


if __name__ == "__main__":
    main()
