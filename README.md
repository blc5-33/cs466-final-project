# CS466 Final Project - Fall 2024

## Instructions to Run Implementations
Space efficient local alignment is implemented under the folder `local-align-hirschberg`, there is a README in that file for running the CLI tool, and a Jupyter Notebook that guides the construction of the CLI tool.

Viral phylogney tree is located under the folder `viral-phylogeny` and again there's a README for that there.

The human coronavirus genomes we have are contained in a the file `scrubbed-viral-data/scrubbed_sequences.csv`.

### Python Environment Setup

Run:
```
$ python3 -m venv .
```
with Python version 3.9 (may work without exactly 3.9? not sure) to create a virtualenv in the same directory as this README file.

Activate it with:
```
$ source ./bin/activate
```
if using Bash/Zsh in terminal (or VS Code).

Run:
```
pip3 install -r requirements.txt
```
to get dependencies installed. Now the components should be runnable. Follow the READMEs in both folders.
