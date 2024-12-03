# CSCE-642: Deep Reinforcement Learning

## Fall 2024 - Final Project

This repository constains code for Floorplanning using RL-based algorithm. The floorplanning is critical in the EDA (Electronic Design Automation). It usually optimizes wirelength and area of the chip design. Here, we use GSRC benchmark to evaluate our implementation.

## Setup

Run the command to set dependencies required in your system
```bash
sudo apt-get install swig build-essential python-dev python3-dev
```
and on Mac by running
```bash
brew install swig
```
or on windows by following the instructions [here](https://open-box.readthedocs.io/en/latest/installation/install_swig.html).

Use a virtual enviroment using conda + pip or virtual env + pip. The Python environment required is 3.9.16 (version)

Install the Python libraryes needed:
```bash
pip install -r requirements.txt
```

## Running

### Floorplanning environment

- `tree_operations.py` script construct the floorplanning and perform operations in the B*-tree representation

- `run.py` script run the episodic training of our RL-based algorithm. For example:

```python
python run.py -s ppo -t 500 -d Floorplan -e 1000 -a 0.001 -g 0.99 -l [30,20] -b 100
```