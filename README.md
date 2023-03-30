# Attiri

Attiri: Tamil Stanford Alpaca. An Instruction-following LLaMA Model

## Table of Contents

- [Preparation](#preparation)
- [Dataset](#dataset)
- [Setup](#setup)
- [Usage](#usage)

## Preparation

This is a Python program that translates instruction data for the Alpaca dataset from one language to another using the Google Translate API. The program is built with Click and tqdm for command-line argument parsing and progress tracking, respectively.

### Dataset

The Alpaca dataset consists of programming problems and their associated input/output examples. The dataset is available in JSON format, with each problem represented by a dictionary containing the following keys:

instruction: a text description of the problem
input: an example input for the problem
output: the expected output for the problem
program: a sample program that solves the problem (optional)
code: the code used to generate the problem (optional)
The program currently supports translation of the instruction, input, and output fields. The other fields (program and code) are ignored.

### Setup

To use the program, you must have Python 3 and the necessary packages installed. You can install the necessary packages using pip:

Create a new Conda environment with Python 3.9:

```bash
conda create --name attiri python=3.9
```

Activate the new environment:

```bash
conda activate alpaca_translation
```

```bash
pip install -r requirements.txt
```

To run the program, use the following command:

```bash
python attiri_data.py -s [SOURCE] -t [TARGET] [INPUT FILE] [OUTPUT FILE]
```

Replace [SOURCE] with the source language you want to translate from (e.g. en for English), [TARGET] with the target language you want to translate to (e.g. fr for French), [INPUT FILE] with the path to the JSON input file, and [OUTPUT FILE] with the path to the JSON output file.

The -s option is optional and will default to automatic language detection if not specified. Note that the input file must exist, but the output file will be created by the program if it does not already exist. If the output file already exists, it will be overwritten.

### Usage

Here are some examples of how to use the program:

Translate data from alpaca_data.json in English to French and save it to output.json:

```bash
python attiri_data.py -s en -t fr alpaca_data.json output.json
```

Translate data from alpaca_data.json in English to Spanish and save it to alpaca_data_es.json:

```bash
python attiri_data.py -s en -t es alpaca_data.json alpaca_data_es.json
```

Automatically detect the source language and translate to German, saving the output to output.json:

```bash
python attiri_data.py -t de alpaca_data.json output.json
```

Note that the program may take some time to run, especially for large input files or when translating to many different languages.
