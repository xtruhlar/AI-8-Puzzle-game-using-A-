import sys
from timeit import default_timer as timer


# This function loads the puzzle inputs from a text file
def load_inputs_from(file_name):
    inputs_list = []
    with open(file_name) as file:
        for line in file:
            inputs_list.append(line.strip())
    return inputs_list


inputs = load_inputs_from("IO/inputs.txt")


# This function converts a string representation of the puzzle into a tuple of tuples
def tuplestring(string):
    # Parse the string and convert it into a list of lists
    board_list = [[int(string[i:i + 3][j]) for j in range(3)] for i in range(0, 9, 3)]
    # Convert the list of lists into a tuple of tuples
    return tuple(tuple(row) for row in board_list)


# Movement and operators for the puzzle
def move(board, operator):
    # Find the position of the empty space (represented by 0)
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                empty_row, empty_col = x, y

    # Create a copy of the current board to modify
    new_state = [list(row) for row in board]

    # Perform a move based on the specified operator ('L' for left, 'R' for right, 'U' for up, 'D' for down)
    if operator == 'R':
        # Move the empty space left if possible
        if empty_col > 0:
            new_state[empty_row][empty_col], new_state[empty_row][empty_col - 1] = \
                new_state[empty_row][empty_col - 1], new_state[empty_row][empty_col]
            return tuple(tuple(row) for row in new_state)

    elif operator == 'L':
        # Move the empty space right if possible
        if empty_col < 2:
            new_state[empty_row][empty_col], new_state[empty_row][empty_col + 1] = \
                new_state[empty_row][empty_col + 1], new_state[empty_row][empty_col]
            return tuple(tuple(row) for row in new_state)

    elif operator == 'D':
        # Move the empty space up if possible
        if empty_row > 0:
            new_state[empty_row][empty_col], new_state[empty_row - 1][empty_col] = \
                new_state[empty_row - 1][empty_col], new_state[empty_row][empty_col]
            return tuple(tuple(row) for row in new_state)

    elif operator == 'U':
        # Move the empty space down if possible
        if empty_row < 2:
            new_state[empty_row][empty_col], new_state[empty_row + 1][empty_col] = \
                new_state[empty_row + 1][empty_col], new_state[empty_row][empty_col]
            return tuple(tuple(row) for row in new_state)

    return None


# Calculate the Manhattan distance h between two puzzle states
def manhattan_distance(board, goal_board):
    h = 0
    for x in range(3):
        for y in range(3):
            if board[x][y] != 0:
                # Find the coordinates of the current tile in the goal board
                goal_row, goal_col = find_tile(goal_board, board[x][y])
                # Calculate the Manhattan distance for the current tile
                h += abs(x - goal_row) + abs(y - goal_col)
    return h


# Helper function to find the coordinates of a tile in a puzzle board
def find_tile(board, tile):
    for x in range(3):
        for y in range(3):
            if board[x][y] == tile:
                return x, y


def hamming(board, goal_board):
    n = 0
    for x in range(3):
        for y in range(3):
            if board[x][y] != goal_board[x][y]:
                n += 1
    return n


# Node class represents each node in the A* search tree
class Node:
    def __init__(self, board, parent=None, operator=None, g=0):
        self.board = board
        self.parent = parent
        self.operator = operator
        self.g = g
        self.h = manhattan_distance(board, goal_state)
        self.f = self.g + self.h
        self.n = hamming(board, goal_state)


def a_algorithm(initial, goal_board):
    open_set = []  # priority queue of !nodes!
    closed_set = set()  # set of visited !states!

    # Create the initial node and set the initial heuristic
    initial_node = Node(initial)
    if heuristic == 1:
        initial_node.h = manhattan_distance(initial, goal_board)
    elif heuristic == 2:
        initial_node.n = hamming(initial, goal_board)
    else:
        print("Invalid input.")
        return None

    open_set.append(initial_node)
    times = timer()

    while open_set:
        # Find the node with the lowest priority (lowest g + h or n)
        if heuristic == 1:
            current = min(open_set, key=lambda node: node.g + node.h)
        elif heuristic == 2:
            current = min(open_set, key=lambda node: node.n)

        if current.board == goal_board:
            return reconstruct_path(current), closed_set  # Goal board reached

        open_set.remove(current)
        closed_set.add(current.board)

        # Generate successor nodes and add them to the open set
        for operator in ['L', 'R', 'U', 'D']:
            next_state = move(current.board, operator)
            if next_state is None or next_state in closed_set:
                continue
            successor = Node(next_state, current, operator, current.g + 1)
            if heuristic == 1:
                successor.h = manhattan_distance(next_state, goal_board)
            elif heuristic == 2:
                successor.n = hamming(next_state, goal_board)
            open_set.append(successor)
        # Check the time limit
        timee = timer()
        if (timee - times) > time_limit_seconds:
            return None

    return None


# Reconstruct the path from the goal node to the initial node
def reconstruct_path(node):
    path = []
    while node is not None:
        path.append(node.operator)
        node = node.parent
    path.reverse()
    path.remove(path[0])
    return path


def print_board(board1, board2):
    """
    Funckia, ktorá orámuje jednotlivé políčka je od autora: ChatGPT-3.5
        Prompt, ktorý som použil:
            'I have table 3*3 and need to create boarders for each cell in console using python'

        Kód, ktorý som dostal a upravil na výsledný kód:
            'print("+" + "-" * 7 + "+")
            for i in range(3):
            print("|", end=' ')
                for j in range(3):
                    print(board[i][j], end=' ')
                print("|")
            print("+" + "-" * 7 + "+")'
    """
    print("┍" + "━" * 3 + "┯" + "━" * 3 + "┯" + "━" * 3 + "┑" + "           " + "┍" + "━" * 3 + "┯" + "━" * 3 + "┯" + "━" * 3 + "┑")
    for x in range(3):
        for y in range(3):
            if y > 0 and board1[x][y - 1] != ' ':
                if board1[x][y] == 0:
                    print(" ", end=' ')
                else:
                    print(board1[x][y], end=' ')
            else:
                if board1[x][y] == 0:
                    print("│ " + " ", end=' ')
                else:
                    print("│ " + str(board1[x][y]), end=' ')
            if y < 2:
                print("│", end=' ')
            if y == 2:
                print("│", end=' ')
        print("   ", end=' ')
        for y in range(3):
            if y > 0 and board2[x][y - 1] != ' ':
                if board2[x][y] == 0:
                    print(" ", end=' ')
                else:
                    print(board2[x][y], end=' ')
            else:
                if board2[x][y] == 0:
                    print("      │ " + " ", end=' ')
                else:
                    print("      │ " + str(board2[x][y]), end=' ')
            if y < 2:
                print("│", end=' ')
            if y == 2:
                print("│", end=' ')
        print()
        if x < 2:
            print("┝" + "━" * 3 + "╂" + "━" * 3 + "╂" + "━" * 3 + "┥" + "   ---->   " + "┝" + "━" * 3 + "╂" + "━" * 3 + "╂" + "━" * 3 + "┥")
    print("┖" + "━" * 3 + "┻" + "━" * 3 + "┻" + "━" * 3 + "┙" + "           " + "┖" + "━" * 3 + "┻" + "━" * 3 + "┻" + "━" * 3 + "┙")


count = 0
time_limit_seconds = 50  # Set your time limit in seconds here

with open("IO/output-hamming.txt", "w", encoding="utf-8") as output_file:
    for i in inputs:
        count = count + 1
        start = i
        initial_state = tuplestring(start)
        goal = '123456780'
        goal_state = tuplestring(goal)

        # Manhattan distance
        # heuristic = 1

        # Hamming distance
        heuristic = 2

        # Call the A* search function to solve the puzzle
        time_start = timer()
        solution_path, closed_set = a_algorithm(initial_state, goal_state)
        time_end = timer()

        orig_stdout = sys.stdout
        sys.stdout = output_file
        if (time_end - time_start) > time_limit_seconds or solution_path is None:
            print(str(count) + ':' + i)
            print_board(initial_state, goal_state)
            print("This puzzle is not solvable.")
            print("\n----------------------------\n")
            continue
        else:
            # Print the solution path or a message if no solution was found
            if solution_path:
                print(str(count) + ':' + i)
                print_board(initial_state, goal_state)
                print("Solution Path:", solution_path)
                print("Number of nodes in path:", solution_path.__len__())
                print("Number of nodes created: ", closed_set.__len__())
                print("Time taken:", (time_end - time_start) * 1000, "ms")
                print("\n----------------------------\n")
            else:
                print("No solution found.")
        sys.stdout = orig_stdout
