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
* **Activation Function**

The activation function that is used for all the nodes except the last layer is the sigmoid function. The activation function used in the last layer is softmax. We use softmax because it makes the agreggated sum of nodes in last layer equal one. 

* **Inputs to the Neural Network**
The inputs to the neural network are
1. The distance of the bird from ground
2. Vertical distance between the bird and the top pipe
3. Vertical distance between the bird and the bottom pipe

* **Output from the Neural Network**

In the last layer we have just one node that tells the bird to either go up or down.
1. if the value of the node is less than 50% we do not go up.
2. if the value is greater than 50% we go up.

### BreakOut
* **Activation Function**

The activation function to all the nodes except the last node is sigmoid function.

* **Inputs to the Neural Network**

The inputs are as follows
1. reactangles x coordinate
2. ball's x coordinate
3. ball's y corrdinate
4. balls starting position

* **Output from the Neural Network**

We have three output nodes in the last layer
1. if the first node has highest probability then we move the rectangle to right.
2. if the second node has highest probability then we move to left.
3. if the third node has highest probability then we do not move it.

## When do the bots die?
The bots never die. Since the bots have been trained for 60 generations each they have become near perfect, they play the game till it is near the end. The flappy bird AI does not die, but the breakOut AI dies before having two or three blocks.

## Inspired from ...
This project was indpired from both TechWithTim and CodeBullet. 

## Demo
* ![GifFlappyBird](https://media.giphy.com/media/hHpha1dLcm3NsLCjBr/giphy.gif)

* ![GifBreakOutAI](https://media.giphy.com/media/doxA29JkeLZg6gfD5u/giphy.gif)

## Credits
* Me
* TheNextCEO
