# NEAT
A NeuroEvolution of Augmenting Topoligies library to evolve a nerual network to perform any task given inputs, outputs, and a fitness function.

## Apps
Currently, Snake and Tetris exist to test the capabilities of the library (and because AI playing games is really cool!)
Below is one of the better results from using the library to learn to play Snake

![](https://media.giphy.com/media/1g1bbHK2MC9fpb4ap6/giphy.gif)

Haven't been able to get a great Tetris model going, but I'm working on it!

## Usage
Make sure you are using Python3.6+ (for the sweet sweet fstrings)
#### Setup
Install the dependancies using pip
`pip install -r requirements.txt`

Make sure the root directory of the repo is in the python path, as we will run everything from there
`export PYTHONPATH=$PYTHONPATH:.` (while in the root directory)

#### Training
To train models for the given apps, simply run their respective `train.py` file. For example, to train Snake

`python apps/snake/train.py`

This will run the algorithm, save the best genome in the genomes directory (in pickle format), and display one game of the model playing.

For those more familiar with NEAT, or if you just want to play around with things, many training configurations can be found at `NEAT/config.py`.

#### Playing
To play the games yourself (to understand the rules or just for fun) run the `play.py` file in any app folder.

To see a genome play run the `play.py` file with the path to the genome as an arg.

For example, to see a game of the snake model (from the GIF), run

`python apps/snake/play.py apps/snake/genomes/pro.pickle`

