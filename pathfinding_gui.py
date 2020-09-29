import a_star
import pygame
import sys


class PathfindingGUI:
    clock = pygame.time.Clock()

    EMPTY = 0
    START = 'A'
    END = 'B'
    OBSTACLE = '*'
    PATH = 'X'
    SUCCESSOR = 1

    DARK_BLUE = (30, 32, 40)
    LIGHT_BLUE = (197, 235, 240)
    WHITE = (250, 250, 250)
    LIGHT_GRAY = (175, 175, 175)
    DARK_GRAY = (50, 50, 50)
    GREEN = (81, 138, 45)
    YELLOW = (247, 238, 166)
    RED = (148, 55, 47)

    def __init__(self, display: pygame.display):
        self.display = display
        self.board = [[self.EMPTY for _ in range(20)] for _ in range(20)]
        self.draw_status = self.OBSTACLE
        self.start_coordinates = (1, 10)
        self.end_coordinates = (18, 10)

    def draw_grid(self) -> None:
        # starts at y = 32, ends at y = 672
        self.board[self.start_coordinates[0]][self.start_coordinates[1]] = self.START
        self.board[self.end_coordinates[0]][self.end_coordinates[1]] = self.END

        def draw_square(sq_color: tuple):
            if 26 * (row + 1) < mouse_pos[0] < 26 * (row + 2) and \
                    3 * 26 + (26 * col) < mouse_pos[1] < 3 * 26 + (26 * col) + 26:
                pygame.draw.rect(self.display, self.LIGHT_GRAY,
                                 ((26 * (row + 1), 3 * 26 + (26 * col)),
                                  (25, 25)))
            else:
                pygame.draw.rect(self.display, sq_color,
                                 ((26 * (row + 1), 3 * 26 + (26 * col)),
                                  (25, 25)))

        mouse_pos = pygame.mouse.get_pos()
        x, y = self.display.get_size()
        colors = {self.EMPTY: self.WHITE, self.OBSTACLE: self.DARK_BLUE, self.SUCCESSOR: self.YELLOW,
                  self.START: self.GREEN, self.END: self.RED, self.PATH: self.LIGHT_BLUE}
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                draw_square(colors[self.board[row][col]])

    def draw_obstacle(self):
        button_font = pygame.font.SysFont('freesansbold.ttf', 48)

        mouse_pos = pygame.mouse.get_pos()
        x, y = self.display.get_size()
        if 26 < mouse_pos[0] < 21 * 26 and 3 * 26 < mouse_pos[1] < 23 * 26:
            a = (mouse_pos[0] - 26) // 26
            b = (mouse_pos[1] - 3 * 26) // 26
            if self.board[a][b] not in {self.START, self.END} and self.draw_status not in {self.START, self.END}:
                self.board[a][b] = self.draw_status

            self.display.blit(button_font.render(str((a, b)), True, self.WHITE), (0, 0))

    def draw_points(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.draw_status in {self.START, self.END} and \
                26 < mouse_pos[0] < 21 * 26 - 8 and 3 * 26 < mouse_pos[1] < 23 * 26 - 8:
            a = (mouse_pos[0] - 26) // 26
            b = (mouse_pos[1] - 3 * 26) // 26
            if self.draw_status == self.START:
                self.board[self.start_coordinates[0]][self.start_coordinates[1]] = self.EMPTY
                self.start_coordinates = a, b
            else:
                self.board[self.end_coordinates[0]][self.end_coordinates[1]] = self.EMPTY
                self.end_coordinates = a, b

    def draw_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        button_font = pygame.font.SysFont('freesansbold.ttf', 48)

        for i in range(2):
            if 810 + (135 * i) < mouse_pos[0] < 925 + (135 * i) and 497 < mouse_pos[1] < 572:
                pygame.draw.rect(self.display, self.LIGHT_GRAY, (800 + (135 * i), 487, 135, 95))
            pygame.draw.rect(self.display, self.WHITE, (810 + (135 * i), 497, 115, 75))

        self.draw_draw_menu()

        self.display.blit(button_font.render('GO', True, self.DARK_BLUE), (841, 519))
        self.display.blit(button_font.render('RESET', True, self.DARK_BLUE), (946, 519))

    def draw_draw_menu(self):
        modes = [(self.START, 0, self.GREEN, 'START'), (self.END, 1, self.RED, 'END'),
                 (self.OBSTACLE, 2, self.DARK_GRAY, 'WALL'), (self.EMPTY, 3, self.DARK_BLUE, 'ERASE')]

        title_font = pygame.font.SysFont('freesansbold.ttf', 60)
        button_font = pygame.font.SysFont('freesansbold.ttf', 48)
        pygame.draw.rect(self.display, self.WHITE, (810, 97, 250, 360))
        self.display.blit(title_font.render('DRAW', True, self.DARK_BLUE), (870, 117))

        mouse_pos = pygame.mouse.get_pos()
        for mode, i, color, title in modes:
            if mode == self.draw_status:
                pygame.draw.rect(self.display, self.LIGHT_GRAY, (830, 167 + (70 * i), 210, 70))

            if 810 < mouse_pos[0] < 1060 and 167 + (70 * i) < mouse_pos[1] < 227 + (70 * i):
                pygame.draw.rect(self.display, self.LIGHT_GRAY, (830, 167 + (70 * i), 210, 70))
            pygame.draw.rect(self.display, color, (840, 177 + (70 * i), 50, 50))
            self.display.blit(button_font.render(title, True, self.DARK_BLUE), (910, 187 + (70 * i)))

        pygame.draw.rect(self.display, self.WHITE, (841, 388, 48, 48))

    def solve(self):
        self.reset()
        node = self.a_star()
        self.clock.tick(45)
        if node:
            path = []
            while node.parent is not None:
                node = node.parent
                path.append((node.x, node.y))
            for i in range(len(path) - 1, -1, -1):
                self.clock.tick(15)
                self.board[path[i][0]][path[i][1]] = self.PATH
                self.draw_grid()
                pygame.display.update()

    def a_star(self):
        open_list = []
        closed_list = []

        # (coordinates: tuple, current_movement_cost: int, f: int)
        open_list.append(a_star.Node(self.start_coordinates, 0, 0))
        while open_list:
            parent = open_list.pop(a_star.find_next_node(open_list))
            for coordinates in a_star.generate_successors(self.board, (parent.x, parent.y)):
                if self.board[coordinates[0]][coordinates[1]] == self.END:
                    return a_star.Node(coordinates, parent.movement_cost + 1, parent.f, parent)

                if self.board[coordinates[0]][coordinates[1]] == self.EMPTY:
                    self.board[coordinates[0]][coordinates[1]] = self.SUCCESSOR
                self.display.fill(self.DARK_BLUE)
                self.draw_grid()
                self.draw_buttons()
                pygame.display.update()

                s_movement_cost = parent.movement_cost + 1
                s_f = s_movement_cost + a_star.manhattan_heuristic(coordinates, self.end_coordinates)

                skip = False
                combined_list = open_list[:]
                combined_list.extend(closed_list)
                for node in combined_list:
                    if coordinates == (node.x, node.y) and node.f <= s_f:
                        skip = True

                if not skip:
                    open_list.append(a_star.Node(coordinates, s_movement_cost, s_f, parent))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 945 < mouse_pos[0] < 1060 and 497 < mouse_pos[1] < 572:
                        open_list = []
                        self.reset()
            closed_list.append(parent)

    def reset(self):
        self.board = \
            [[self.EMPTY if self.board[i][j] != self.OBSTACLE else self.OBSTACLE for j in range(20)] for i in range(20)]


def main():
    pygame.init()
    display_size = (1200, 810)
    display = pygame.display.set_mode(display_size)
    pathfinding = PathfindingGUI(display)

    running = True
    while running:
        display.fill(pathfinding.DARK_BLUE)
        pathfinding.draw_grid()
        pathfinding.draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(4):
                    status = {0: pathfinding.START, 1: pathfinding.END, 2: pathfinding.OBSTACLE, 3: pathfinding.EMPTY}
                    if 810 < mouse_pos[0] < 1060 and 167 + (70 * i) < mouse_pos[1] < 227 + (70 * i):
                        pathfinding.draw_status = status[i]
                if 810 < mouse_pos[0] < 925 and 497 < mouse_pos[1] < 572:
                    pathfinding.solve()
                if 945 < mouse_pos[0] < 1060 and 497 < mouse_pos[1] < 572:
                    pathfinding.reset()
                if 26 < mouse_pos[0] < 21 * 26 - 8 and \
                        3 * 26 < mouse_pos[1] < 23 * 26 - 8:
                    pathfinding.draw_points()
        if pygame.mouse.get_pressed()[0]:
            pathfinding.draw_obstacle()

        pygame.display.update()


main()
