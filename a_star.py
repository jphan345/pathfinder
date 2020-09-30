from pathfinding import *


def manhattan_heuristic(coordinates: tuple, end: tuple) -> int:
    """Estimated movement cost from given square to the destination."""
    return abs(coordinates[0] - end[0]) + abs(coordinates[1] - end[1])


def diagonal_heuristic(coordinates: tuple, end: tuple) -> int:
    return max(abs(coordinates[0] - end[0]), abs(coordinates[1] - end[1]))


def find_next_node(nodes: list) -> int:
    """Return the index of the node with the lowest f (total movement cost)."""
    index = 0
    for i in range(len(nodes)):
        if nodes[i].f < nodes[index].f:
            index = i
    return index


def search(board: list) -> Node:
    """Text-based version of A* pathfinding algorithm."""
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
            combined_list = open_list[:]
            combined_list.extend(closed_list[:])
            for node in combined_list:
                if coordinates == (node.x, node.y) and node.f <= s_f:
                    skip = True

            if not skip:
                open_list.append(Node(coordinates, s_movement_cost, s_f, parent))

        closed_list.append(parent)


def visual_search(self):
    """Visual a_star algorithm."""
    import pygame
    import sys

    open_list = []
    closed_list = []

    # (coordinates: tuple, current_movement_cost: int, f: int)
    open_list.append(Node(self.start_coordinates, 0, 0))
    while open_list:
        parent = open_list.pop(find_next_node(open_list))
        for coordinates in generate_successors(self.board, (parent.x, parent.y)):
            if self.board[coordinates[0]][coordinates[1]] == self.END:
                return Node(coordinates, parent.movement_cost + 1, parent.f, parent)

            if self.board[coordinates[0]][coordinates[1]] == self.EMPTY:
                self.board[coordinates[0]][coordinates[1]] = self.SUCCESSOR

            self.display.fill(self.DARK_BLUE)
            self.draw_grid()
            self.draw_buttons()
            pygame.display.update()

            s_movement_cost = parent.movement_cost + 1
            s_f = s_movement_cost + manhattan_heuristic(coordinates, self.end_coordinates)

            skip = False
            combined_list = open_list[:]
            combined_list.extend(closed_list)
            for node in combined_list:
                if coordinates == (node.x, node.y) and node.f <= s_f:
                    skip = True
            if not skip:
                open_list.append(Node(coordinates, s_movement_cost, s_f, parent))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 780 < mouse_pos[0] < 920 and 15 < mouse_pos[1] < 60:
                    open_list = []
                    self.reset()

        closed_list.append(parent)
