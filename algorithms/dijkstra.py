from algorithms.pathfinding import *


def get_next(nodes: list) -> int:
    """Return the index of the node with the lowest movement cost from the start."""
    j = 0
    for i in range(len(nodes)):
        if nodes[i].movement_cost < nodes[j].movement_cost:
            j = i
    return j


def search(board: list) -> Node:
    """Text-based algorithm for Dijkstra's search."""
    start = find_node(board, START)
    end = find_node(board, END)

    open_list = [Node(start, 0, 0)]  # unsolved nodes
    open_list_c = set()
    open_list_c.add(start)
    closed_list = []  # solved nodes
    while open_list:
        index = get_next(open_list)
        parent = open_list.pop(index)
        open_list_c.remove((parent.x, parent.y))
        closed_list.append((parent.x, parent.y))

        for coordinates in generate_successors(board, (parent.x, parent.y)):
            if coordinates == end:
                return Node(coordinates, parent.movement_cost + 1, 0, parent)
            if coordinates not in closed_list and coordinates not in open_list_c:
                if board[coordinates[0]][coordinates[1]] == WEIGHT:
                    open_list.append(Node(coordinates, parent.movement_cost + 6, 0, parent))
                else:
                    open_list.append(Node(coordinates, parent.movement_cost + 1, 0, parent))


def visual_search(self) -> Node:
    """Visually displays Dijkstra's search algorithm.
    variables:: self.display, self.board, self.start_coordinates, self.end_coordinates, self.EMPTY, self.SUCCESSOR,
                self.DARK_BLUE
    functions:: self.draw_grid, self.draw_buttons, self.reset"""
    import pygame
    import sys

    open_list = [Node(self.start_coordinates, 0, 0)]
    open_list_c = set()
    open_list_c.add(self.start_coordinates)
    closed_list = []

    while open_list:
        parent = open_list.pop(get_next(open_list))
        closed_list.append((parent.x, parent.y))
        if self.board[parent.x][parent.y] == self.EMPTY:
            self.board[parent.x][parent.y] = self.SUCCESSOR
        if self.board[parent.x][parent.y] == self.WEIGHT:
            self.board[parent.x][parent.y] = self.WEIGHTED_SUCCESSOR

        for coordinates in generate_successors(self.board, (parent.x, parent.y)):
            if coordinates == self.end_coordinates:
                return Node(coordinates, parent.movement_cost + 1, parent.f, parent)

            self.display.fill(self.DARK_BLUE)
            self.draw_grid()
            self.draw_buttons()
            pygame.display.update()

            if coordinates == self.end_coordinates:
                return Node(coordinates, parent.movement_cost + 1, 0, parent)
            combined_list = open_list[:]
            combined_list.extend(closed_list[:])
            if coordinates not in combined_list and coordinates not in open_list_c:
                if self.board[coordinates[0]][coordinates[1]] == self.EMPTY:
                    open_list.append(Node(coordinates, parent.movement_cost + 1, 0, parent))
                else:
                    open_list.append(Node(coordinates, parent.movement_cost + 6, 0, parent))
                open_list_c.add(coordinates)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 780 < mouse_pos[0] < 920 and 15 < mouse_pos[1] < 60:
                    open_list = []
                    self.reset()
