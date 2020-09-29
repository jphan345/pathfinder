START = 'A'
END = 'B'
OBSTACLE = '*'


class Node:
    def __init__(self, coordinates: tuple, movement_cost: int, f: int, parent=None):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.movement_cost = movement_cost
        self.f = f
        self.parent = parent  # Node


def a_star(board: list):
    open_list = []
    closed_list = []

    start_coordinates = find_node(board, START)
    end_coordinates = find_node(board, END)

    open_list.append(Node(start_coordinates, 0, 0))  # (coordinates: tuple, current_movement_cost: int, f: int)

    while len(open_list):
        parent = open_list.pop(find_next_node(open_list))

        for coordinates in generate_successors(board, (parent.x, parent.y)):
            if board[coordinates[0]][coordinates[1]] == END:
                return Node(coordinates, parent.movement_cost + 1, parent.f, parent)

            s_movement_cost = parent.movement_cost + 1
            s_f = s_movement_cost + manhattan_heuristic(coordinates, end_coordinates)

            skip = False
            for node in open_list:
                if coordinates == (node.x, node.y) and node.f < s_f:
                    skip = True
            for node in closed_list:
                if coordinates == (node.x, node.y) and node.f < s_f:
                    skip = True

            if not skip:
                open_list.append(Node(coordinates, s_movement_cost, s_f, parent))

        closed_list.append(parent)


def diagonal_heuristic(coordinates: tuple, end: tuple) -> int:
    """Estimated movement cost from given square to the final destination."""
    return max(abs(coordinates[0] - end[0]), abs(coordinates[1] - end[1]))


def manhattan_heuristic(coordinates: tuple, end: tuple) -> int:
    return abs(coordinates[0] - end[0]) + abs(coordinates[1] - end[1])


def find_node(board: list, node_name: str) -> tuple:
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == node_name:
                return row, col


def find_next_node(nodes: list) -> int:
    """Return the index of the node with the lowest f (total movement cost)."""
    index = 0
    for i in range(len(nodes)):
        if nodes[i].f < nodes[index].f:
            index = i
    return index


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

    # Yield the diagonal successors
    for i in [1, -1]:
        for j in [1, -1]:
            x, y = coordinates[0] + i, coordinates[1] + j
            if check(x, y) and check_diagonal(coordinates, (x, y)):
                yield x, y


def print_board(board: list) -> None:
    for i in board:
        for j in i:
            if j == START or j == END:
                print(f'*{j}*', end='')
            else:
                print(f' {j} ', end='')
        print()


if __name__ == '__main__':

    test = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, START, 0, 0, 0, 0, 0, 0, 0, 0, END, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    test2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, START, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, END, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
             ]

    n = a_star(test2)

    n = n.parent
    while n.parent:
        test2[n.x][n.y] = 'X'
        n = n.parent

    # X is used to denote the path from A to B
    # * is used to denote a wall that the path cannot go through
    # 0 is an empty spot
    print_board(test2)
