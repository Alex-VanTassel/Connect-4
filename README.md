# Project: Testing the performance of different learning agents in Connect 4

In this project, I implement numerous learning agents, and test their performance against each other

- Agents
    - Random
        - Selects moves at random
    - Human
        - Requests user input for moves (implemented moreso to have fun with)
    - Q-learning
        - Agent takes a period of time (given as an argument to the agents initializer) to learn the game (plays against the random agent while doing so), and then proceeds to play optimal moves according to its understanding of the game
        - The agents knowledge of the game is limited, and hence when it encounters a new game state, the agent selects a move at random
        - Future enhancement: give small rewards for agent placing chips in squares with a larger number of possible connect 4's
            - Should be able to get the agents behavior to converge to an optimal policty sooner
    - Monte-Carlo Tree Search
        - Agent takes a period of time to learn, and then uses its understanding of the game to make moves
        - Again its knowledge will be limited, so it will randomly select actions when in a state the agent hasn't explored already
    - Neural Network (Coming soon)
        - Train neural network to make moves at given game states

Selection of agents, and game iterations can be modified in the 'main.py' file. The rest of the files contain implementations of the different components of the project