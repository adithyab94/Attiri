<p align="center" width="100%">
<a href="https://adithyabalaji.notion.site/Attiri-A-LLaMa-Model-for-Tamil-d49b91e2d7704c3286fd4ac4c1934c18" target="_blank"><img src="assets/attiri_logo.png" alt="Stanford-Alpaca" style="width: 50%; min-width: 300px; display: block; margin: auto;"></a>
</p>

<h1 align="center">
  <br />
  Attiri: Dataset and an instruction-following large language model for Tamil by unlocking LLaMa and Stanford Alpaca
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

## TODO

- The code for fine-tuning the model.

## Table of Contents

1. [Preparation](#preparation)
   1. [Setup](#setup)
   2. [Dataset](#dataset)
2. [Usage](#usage)
3. [License](#license)

## Preparation

### Setup

To use the program, you must have Python 3 and the necessary packages installed. You can install the necessary packages using pip:

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
| 1    | [Alpaca](data/attiri_alpaca_data.json)  | Tamil version of the Stanford Alpaca dataset | 52K| Instruction, Input, Output|
| 2    | [Nomic]()  | Tamil version of the Nomic dataset | 500K | Prompt, Response|
| 3    | [IndicCorp](https://ai4bharat.iitm.ac.in/corpora)| A single large text file containing one sentence per line. The publicly released version is randomly shuffled, untokenized and deduplicated. | 31.5M| Sentences|

``attiri_data.py`` translates instruction data for the Alpaca dataset from one language to another using the Google Translate API. The program is built with Click and tqdm for command-line argument parsing and progress tracking, respectively.

To run the program, use the following command:

```bash
python attiri_data.py -s [SOURCE] -t [TARGET] -d [DATASET] [INPUT FILE] [OUTPUT FILE]
```

Replace [SOURCE] with the source language you want to translate from (e.g. en for English), [TARGET] with the target language you want to translate to (e.g. fr for French), [INPUT FILE] with the path to the JSON input file, and [OUTPUT FILE] with the path to the JSON output file. Replace [DATASET] with the dataset you want to translate (e.g. ``alpaca`` or ``nomic``).

The -s option is optional and will default to automatic language detection if not specified. Note that the input file must exist, but the output file will be created by the program if it does not already exist. If the output file already exists, it will be overwritten.

## Usage

Here are some examples of how to use the program:

Translate data from alpaca_data.json in English to French and save it to output.json:

```bash
python attiri_data.py -s en -t fr -d alpaca alpaca_data.json output.json
```

Note that the program may take some time to run, especially for large input files or when translating to many different languages.

## Acknowledgments

Thanks for the open source projects - [LLaMA](https://github.com/facebookresearch/llama), [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca), and [Alpaca-Lora](https://github.com/tloen/alpaca-lora) from which this project is inspired.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
