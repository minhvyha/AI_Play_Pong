# **AI Play Pong With NEAT**

## **Video Demo:**
##[Watch it](https://youtu.be/JI2hABcPUBY)

## **Description:**

### Technologies used:

- Pygame
- Python
- NEAT

### Concepts in the project:

- Data strucutre (list, tuple)
- Object-Oriented Programming (OOP)
- Conditional and loop statements
- Function from pygame library
- NEAT functions

### About this project
This project using NEAT (**NeuroEvolution of Augmenting Topologies**) to build and train an AI to play a simple game (Pong). I implemented all the interface of the game and the algorithms to play the game. The AI building and training is supported by YouTuber 'Tech With Tim'.
\
\
The AI receive three different inputs and output one of three different instructions. AI receives the coordinate of its paddle, coordinate of the ball and the exact distance from its paddle to the ball and decide if the paddle will stay still, move up or down. Whenever its paddle hit the ball, the AI fitness get increase and when the paddle miss the ball, its fitness score get deducted. Some of the worst AI will get removed and the AI with the highest fitness score will be combined to produce a new generation to continue.
### What I learn
During this project, I have an opportunity to work with NEAT a library to simulate neural network for machine learning. I have learnt that the 
**Note: pygame and NEAT library need to be installed before running this project.**
