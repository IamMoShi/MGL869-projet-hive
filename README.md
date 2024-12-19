# School Lab - ETS Montreal - Master's Degree - MGL869

Autumn 2024

---

## Summary

This repository contains the code for the school lab of the MGL869 course at ETS Montreal.
The goal of this lab is to implement simple version of algorithms "logistic regression" and "random forest" to predict
bugs in software [Hive](https://hive.com/).
---

## Lesson

[MGL869-01 Sujets spéciaux I : génie logiciel (A2024)](https://www.etsmtl.ca/etudes/cours/mgl869-a24)

## Authors

- Léo FORNOFF [leo.fornoff.1@ens.etsmtl.ca]() # Author of the project
- William PHAN [william.phan.1@ens.etsmtl.ca]() # Co-author of the lab
- Yannis OUAKRIM [yannis.ouakrim.1@ens.etsmtl.ca]() # Co-author of the lab

## Supervisor

- Mohammed SAYAGH, Ph.D., AP

---

## Table of contents

- [Get started](#get-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Project structure](#project-structure)

## Get started

### Prerequisites

- Python 3.11 or 3.12
- Pip
- Virtualenv
- Required packages (see [requirements.txt](requirements.txt))
- Git
- [Scitools Understand](https://scitools.com/)

### Installation

1. Clone the repository
2. Create a virtual environment and activate it ([doc](https://docs.python.org/3/library/venv.html))
3. Install the required packages

```bash
pip3 install -r requirements.txt
```

> Note: You may need to adapt according to your system
> For MacOS users, compatible Python versions are up to 3.12. Do not use 3.13 or later versions.

4. Adapte configuration file `config.ini` to your environment. Especially, you need to set the path to the `und`
   executable of Understand.
5. To shorten the execution time, you can download the metrics from [here](https://drive.google.com/file/d/1uRyOtRW6DEP8dJssh1PNcvswg-lBCMdN/view?usp=drive_link). Otherwise,
   you may need to adapt the path to the metrics in the configuration file `config.ini` to rebuild the metrics.
6. Run the Jupyter Notebook

```bash
jupyter notebook
```

7. Open the notebook 'run.ipynb' and run the cells

> First run will take a lot of time because it will clone the repo, download the dataset and run the analysis.


files to run are in the main directory. The correct order is to run:
1. data_extraction_lab.ipynb
2. understand_metrics.ipynb
3. evolution_metrics.ipynb

After that, all the data should be stored locally and accessible for all the other notebooks and python scripts in the main directory.