# maze-solver
See if an AI using Q Learning can solve your maze.

## how to use
1. Install pygame and numpy

   ```
   pip install pygame
   ```
   ```
   pip install numpy
   ```

2. Run main.py (using Python 3) from the appropriate directory

   ```
   python3 main.py
   ```
   
3. Build a maze and watch the AI try and solve it!

## tips & tricks
1. While training you will see a "##.#% Random" label. The percentage should continually decrease, however if you would like your AI to explore the maze a little more, press SPACE to pause the decrease of this value and let the AI take more random moves. (the percentage is 100 times the epsilon value used for the epsilon-greedy strategy)
2. As of now, there isn't any way to resize the maze from in the game. However, if you would like to, open main.py in an editor and search for the first occurence of **BOARD_WIDTH** and **BOARD_HEIGHT**. Change their assignment to your desired maze (board) size.
3. Also, without pauses in the decrease of the % Random value, it currently takes about 5 minutes on ×8 speed on my machine to reach 0% Random moves (where the AI just does the move it has found to be best in that situation, rather than picking a random move). If you would like this to not take so long, open entities.py in an editor and search for the first occurrence of **DELTA_EPSILON** and change it to a slightly larger value. (this might impact the AI's performance on the maze as it will have less time to explore it)

   **side note:** hopefully one day these values can be changed in game

## project history
I had tried to implement Q Learning in the _rocket-evolution_ project but it did not work as expected. However, I definitely wanted to attempt to complete a project that used this form of reinforcement learning so I settled on this maze solver.

Originally, I thought the maze would just randomly generate and the user would simply sit back and watch the AI try and solve the maze, however it became apparent that having some sort of UI would be more fun!

Thankfully, while creating the game and its behaviour, there were very few hiccups. However, this changed when implementing the initial version of the Q Learning Algorithm.

At first, I never gave the player enough time to explore the maze which resulted in spotty results when left to its own devices (when the Random move percentage reached 0%). In an attempt to fix this issue, I gave the player a sort of sense of 'smell' in that it could determine which direction the reward (yellow square) was. Yet when I tested this player against some trickier mazes (where you may have to go backwards first in order to reach the goal), it could not learn them. Finally, I reverted back to the original implementation of the algorithm but gave the player more time to explore, eventually leading to desireable results.



