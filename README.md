# AI Bot playing Games
* FlappyBird
* BreakOut
* How to run?
* How does it work?
* When do they die?
* Libraries Used
* Inspired From...
* Demo

## FlappyBird
![FlappyBird](/pics/FlappyBird.png)

## BreakOut
![BreakOut](/pics/BreakOut.png)

## How to run?
To run this project it is enough to download the src folder and to run the 'AIBreakOut.py' and 'AIFlappyBird.py'. 

## How does it work?
To create an AI we first have to train it. Both these bots were trained using NEAT algorithm, this requires a config file that descirbe what parameters to train the AI on. After the training is complete, we save the model in a pickle file. This file stores the neural network in a binary format, which includes all the nodes, their connection and weights. When we run the python file the program simply uses the pickle file and plays the game.

### Flappy Bird
* Activation Function
* Inputs to the Neural Network
* Output from the Neural Network

### BreakOut
* Activation Function
* Inputs to the Neural Network
* Output from the Neural Network

## When do the bots die?
The bots never die. Since the bots have been trained for 60 generations each they have become near perfect, they play the game till it is over.

## Inspired from ...
This project was indpired from both TechWithTim and CodeBullet. 
## Demo
