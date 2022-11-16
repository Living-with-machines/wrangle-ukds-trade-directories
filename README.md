# Wrangle UKDA Trade Directories

Code in this repository can be used to consolidate UKDA Trade Directories and metadata into a better file structure in advance of a workshop in December 2022.

## Installation

First, make sure you have Poetry installed locally.

Then, in this repository, run:

```sh
$ poetry install
```

## How to run

Enter the Poetry shell:

```sh
$ poetry shell
```

Once in there, you can run the tool this way:

```sh
$ python -m wrangle_ukds_trade_directories --input PATH-TO-UKDA-FILES-DIRECTORY --output UKDS-consolidated --metadata PATH-TO-cdm_metadata_cleaned.csv
```
