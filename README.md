# AI-8-Puzzle-game-using-A-star

Defining Problem
Our task is to solve the 8-puzzle, a game involving 8 numbered tiles and an empty space. Tiles can be moved in four directions, but only if an empty space allows it. Each puzzle has an initial and target position, and the objective is to find a sequence of moves to transition from one to the other.

![image](https://github.com/user-attachments/assets/c1bca426-faf3-45d2-b9d2-5c9d29b6c8d7)


Implementation
When solving this problem using state-space search algorithms, we need to specify certain concepts:
State
A state represents the current tile arrangement. The initial state can be represented as ((1 2 3)(4 5 6)(7 8 m)) or (1 2 3 4 5 6 7 8 m), each with its own advantages.
Operators
There are four operators: RIGHT, DOWN, LEFT, and UP. Operators transform a state if possible. All operators have equal weight.
Heuristic Function
Some algorithms require additional information in the form of a heuristic, estimating the distance from the current state to the goal state. Several heuristics are available, like tile count not in place or sum of distances of each tile from its goal. Avoid including the empty space in these calculations.

![image](https://github.com/user-attachments/assets/1c78f2ca-5e80-4e39-bc3b-043240b599a0)


Node
To visualize the path, we create a graph from the state space, typically a tree. States become nodes with attributes such as state representation and parent reference. Nodes can also store operator history, depth, path cost, and estimated cost to the goal.
ALGORITHM
1. Create an initial node and place it among the generated but unprocessed nodes.
2. If there are no generated and unprocessed nodes, terminate with failure - no solution exists.
3. Select the most suitable node from the generated and unprocessed nodes, label it as the current node.
4. If this node represents the goal state, terminate with success - output the solution.
5. Create successors of the current node and add them to the processed nodes.
6. Sort the successors and store them among the generated but unprocessed nodes.
7. Go to step 2.
