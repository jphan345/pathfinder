# File with functions needed for each pathfinding algorithm

START = 'A'
END = 'B'
OBSTACLE = '*'
WEIGHT = 'W'


class Node:
    def __init__(self, coordinates: tuple, movement_cost: int, f: int, parent=None):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.movement_cost = movement_cost
        self.f = f
        self.parent = parent  # Node


def find_node(board: list, node_name: str) -> tuple:
    """Find a node in the board and return the coordinates."""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == node_name:
                return row, col


def generate_successors(board, coordinates) -> tuple:
    """Generate the given node's successors.
    Yield the horizontal and vertical successors before the diagonal successors."""

    def check(coord_x: int, coord_y: int) -> bool:
        # Checks to see if a coordinate is valid to move to
        return 0 <= coord_x <= len(board) - 1 and 0 <= coord_y <= len(board[coord_x]) - 1 and \
               (coord_x, coord_y) != coordinates and board[coord_x][coord_y] != OBSTACLE

    def check_diagonal(coord_1: tuple, coord_2: tuple) -> bool:
        # Checks a diagonal to see if the path can go there.
        # Used to prevent cases where the path goes through a wall that is connected together by its corners.
        x_diff = coord_2[0] - coord_1[0]
        y_diff = coord_2[1] - coord_1[1]
        return board[coord_1[0] + x_diff][coord_1[1]] != OBSTACLE or board[coord_1[0]][coord_1[1] + y_diff] != OBSTACLE

    # Yield the horizontal and vertical successors
    for i in [1, -1]:
        x, y = coordinates[0] + i, coordinates[1] + i
        if check(x, coordinates[1]):
            yield x, coordinates[1]
        if check(coordinates[0], y):
            yield coordinates[0], y

    '''# Yield the diagonal successors
    for i in [1, -1]:
        for j in [1, -1]:
            x, y = coordinates[0] + i, coordinates[1] + j
            if check(x, y) and check_diagonal(coordinates, (x, y)):
                yield x, y'''


def print_board(board: list) -> None:
    for i in board:
        for j in i:
            if j == START or j == END:
                print(f'*{j}*', end='')
            else:
                print(f' {j} ', end='')
        print()
