from typing import Dict, List
from deep_translator import GoogleTranslator
from tqdm import tqdm

import json
import click


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
            self.data = {ind : item for ind, item in enumerate(self.data_raw)}

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
                        translated_data["input"] = my_translator.translate(text=data["input"])
                    if data["output"].isnumeric():
                        translated_data["output"] = data["output"]
                    else:
                        translated_data["output"] = my_translator.translate(text=data["output"])
            yield translated_data




@click.command()
@click.option("--source", "-s", default="auto", help="Source language (default: auto)")
@click.option("--target", "-t", required=True, help="Target language")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def main(source: str, target: str, input_file: str, output_file: str) -> None:
    data = AlpacaDataProcessor(input_file)
    data.load()
    data.get_translated_dict_list(source=source, target=target)
    data.save(output_file)


if __name__ == "__main__":
    main()