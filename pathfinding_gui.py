import a_star
import pygame
import sys


class PathfindingGUI:

    EMPTY = 0
    START = 'A'
    END = 'B'
    OBSTACLE = '*'
    PATH = 'X'
    SUCCESSOR = 1

    DARK_BLUE = (30, 32, 40)
    BLUE = (85, 180, 217)
    WHITE = (250, 250, 250)
    LIGHT_GRAY = (140, 140, 140)
    GRAY = (100, 100, 100)
    DARK_GRAY = (50, 50, 50)
    GREEN = (81, 138, 45)
    YELLOW = (247, 238, 166)
    RED = (148, 55, 47)

    clock = pygame.time.Clock()

    def __init__(self, display: pygame.display):
        self.display = display
        self.board_size = (48, 30)
        self.board = [[self.EMPTY for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.draw_status = self.OBSTACLE
        self.start_coordinates = (3, 15)
        self.end_coordinates = (45, 15)
        self.paths_exist = False

    def set_target_points(self):
        """Set the start and end points onto the board."""
        self.board[self.start_coordinates[0]][self.start_coordinates[1]] = self.START
        self.board[self.end_coordinates[0]][self.end_coordinates[1]] = self.END

    def draw_grid(self) -> None:
        """Draw the board."""
        def draw_square(sq_color: tuple):
            if 26 * (row + 1) < mouse_pos[0] < 26 * (row + 2) and \
                    75 + (26 * col) < mouse_pos[1] < 75 + (26 * (col + 1)):
                pygame.draw.rect(self.display, self.LIGHT_GRAY, ((26 * (row + 1), 75 + (26 * col)), (25, 25)))
            else:
                pygame.draw.rect(self.display, sq_color, ((26 * (row + 1), 75 + (26 * col)), (25, 25)))

        colors = {self.EMPTY: self.WHITE, self.OBSTACLE: self.DARK_GRAY, self.SUCCESSOR: self.YELLOW,
                  self.START: self.GREEN, self.END: self.RED, self.PATH: self.BLUE}

        self.set_target_points()
        mouse_pos = pygame.mouse.get_pos()
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                draw_square(colors[self.board[row][col]])

    def draw_obstacle(self):
        """Draw an obstacle the path has to go around."""
        if self.paths_exist:
            self.reset()

        mouse_pos = pygame.mouse.get_pos()
        row = len(self.board)
        col = len(self.board[row - 1])

        if 26 < mouse_pos[0] < (row + 1) * 26 and 75 < mouse_pos[1] < 75 + col * 26:
            a = (mouse_pos[0] - 26) // 26
            b = (mouse_pos[1] - 75) // 26
            if self.board[a][b] not in {self.START, self.END} and self.draw_status not in {self.START, self.END}:
                self.board[a][b] = self.draw_status

    def draw_points(self):
        """Move the start or end points to where the mouse position is."""
        mouse_pos = pygame.mouse.get_pos()
        row = len(self.board)
        col = len(self.board[row - 1])

        if self.draw_status in {self.START, self.END} and \
                26 < mouse_pos[0] < (row + 1) * 26 and 75 < mouse_pos[1] < 75 + col * 26:
            a = (mouse_pos[0] - 26) // 26
            b = (mouse_pos[1] - 75) // 26

            if self.draw_status == self.START:
                self.board[self.start_coordinates[0]][self.start_coordinates[1]] = self.EMPTY
                self.start_coordinates = a, b
            else:
                self.board[self.end_coordinates[0]][self.end_coordinates[1]] = self.EMPTY
                self.end_coordinates = a, b

    def draw_buttons(self):
        """Draw the clickable buttons."""
        mouse_pos = pygame.mouse.get_pos()
        button_font = pygame.font.SysFont('freesansbold.ttf', 48)
        button_font_2 = pygame.font.SysFont('freesansbold.ttf', 42)
        shadow = pygame.Surface((160, 55))
        shadow.fill(self.DARK_BLUE)
        shadow.set_alpha(90)

        pygame.draw.rect(self.display, self.RED, ((570, 10), (160, 55)))
        pygame.draw.rect(self.display, self.WHITE, ((780, 15), (140, 45)))
        self.draw_draw_menu()
        self.display.blit(button_font.render('SEARCH', True, self.WHITE), (579, 22))
        self.display.blit(button_font_2.render('RESET', True, self.DARK_BLUE), (803, 25))

        if 570 < mouse_pos[0] < 730 and 10 < mouse_pos[1] < 65:
            self.display.blit(shadow, (570, 10))
        if 780 < mouse_pos[0] < 920 and 15 < mouse_pos[1] < 60:
            self.display.blit(shadow, (780, 10))

    def draw_draw_menu(self):
        """Draw the 'Draw:' section of the buttons.'"""
        modes = [(self.START, 0, self.GREEN, 'START'), (self.END, 1, self.RED, '  END'),
                 (self.OBSTACLE, 2, self.DARK_GRAY, ' WALL'), (self.EMPTY, 3, self.WHITE, 'ERASE')]

        title_font = pygame.font.SysFont('freesansbold.ttf', 48)
        button_font = pygame.font.SysFont('freesansbold.ttf', 24)
        self.display.blit(title_font.render('DRAW:', True, self.WHITE), (25, 33))

        mouse_pos = pygame.mouse.get_pos()
        for mode, i, color, title in modes:
            if mode == self.draw_status:
                pygame.draw.rect(self.display, self.GRAY, (157 + (70 * i), 5, 70, 65))
            if 157 + (70 * i) < mouse_pos[0] < 227 + (70 * i) and 5 < mouse_pos[1] < 70:
                pygame.draw.rect(self.display, self.LIGHT_GRAY, (157 + (70 * i), 5, 70, 65))

            pygame.draw.rect(self.display, color, (180 + (70 * i), 15, 25, 25))
            self.display.blit(button_font.render(title, True, self.WHITE), (165 + (70 * i), 48))

    def solve(self):
        """Solve the board visually."""
        if self.paths_exist:
            self.reset()

        self.paths_exist = True
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
        """Visual a_star algorithm."""
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
                    if 780 < mouse_pos[0] < 920 and 15 < mouse_pos[1] < 60:
                        open_list = []
                        self.reset()

            closed_list.append(parent)

    def reset(self):
        x, y = self.board_size
        if self.paths_exist:
            self.board = \
                [[self.EMPTY if self.board[i][j] != self.OBSTACLE else self.OBSTACLE for j in range(y)] for i in
                 range(x)]
            self.paths_exist = False
        else:
            self.board = [[self.EMPTY for _ in range(y)] for _ in range(x)]
        self.set_target_points()


def main():
    pygame.init()
    display_size = (1300, 880)
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
                    if 157 + (70 * i) < mouse_pos[0] < 227 + (70 * i) and 5 < mouse_pos[1] < 70:
                        pathfinding.draw_status = status[i]
                if 570 < mouse_pos[0] < 730 and 10 < mouse_pos[1] < 65:
                    pathfinding.solve()
                if 780 < mouse_pos[0] < 920 and 15 < mouse_pos[1] < 60:
                    pathfinding.reset()
                if 26 < mouse_pos[0] < 49 * 26 and 75 < mouse_pos[1] < 75 + 30 * 26:
                    pathfinding.draw_points()

        if pygame.mouse.get_pressed()[0]:
            pathfinding.draw_obstacle()

        pygame.display.update()


main()
