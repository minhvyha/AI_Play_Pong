# **AI_Play_Pong**

## **Video Demo:**
`https://youtu.be/Jdq0lGXcUm4`

## **Description:**

### Technologies used:

- Pygame
- Python
- NEAT (NeuroEvolution of Augmenting Topologies)

### Concepts in the project:
 
- Data strucutre (list, tuple)
- Object-Oriented Programming (OOP)
- Conditional statements
- Function from pygame library

### About this project
I used NEAT library to bulid and train AI to play Pong (A previous game project that I made). I implemented the visual and the algorithms for the basic pong gameplay, and the AI training as well as uses of NEAT library is supported by YouTuber 'Tech With Tim'. I took this project as a first insight to the machine learning and neural network for AI.
\
\
In the project, I implement the process of training and building AI as well as storing and reuse different AI with different difficulty for players to choose to play against at. This AI took 3 inputs, the current y coordinate of its paddle, y coordinate of the ball and the absolute value of the distance of its paddle to the ball. The AI then randomly choose to either move up, down or stay based on its weight. The fitness of the AI then be evaluate by how much time it can hit the ball. Some of the worst performing AI will be removed and the top fitness-score AI will combined to each other and create a new generation. 
\
\
I then took the AI that able to get the score of 400 fitness-score to be the hardest AI to play against at in the game (impossible). I took the AI that able to get teh score of 200 to be Hard, 100 to be Medium and 50 to be Easy.
\
\
Note: pygame library need to be installed before running this project.
