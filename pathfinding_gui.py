from algorithms import a_star, dijkstra, breadth_first_search
import pygame


class Button:

    def __init__(self, dis: pygame.display, coord: tuple, size: tuple, col: tuple, t: str, t_size: int, t_color: tuple):
        self.display = dis
        self.coordinates = coord
        self.size = size
        self.rect_color = col
        self.text = t
        self.font = pygame.font.SysFont('freesansbold.ttf', t_size)
        self.text_color = t_color
        self.text_offset = (0, 0)
        self.hover_color = (30, 32, 40)
        self.button_function = None

    def draw(self):
        pygame.draw.rect(self.display, self.rect_color, (self.coordinates, self.size))

        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=(self.coordinates[0] + (self.size[0] // 2) + self.text_offset[0],
                                          self.coordinates[1] + (self.size[1] // 2) + self.text_offset[1]))
        self.display.blit(text, text_rect)
        self.hover()

    def hover(self):
        if self.is_on():
            shadow = pygame.Surface(self.size)
            shadow.fill((30, 32, 40))  # Dark blue
            shadow.set_alpha(90)
            self.display.blit(shadow, self.coordinates)

    def is_on(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.coordinates[0] < mouse_pos[0] < self.coordinates[0] + self.size[0] and \
               self.coordinates[1] < mouse_pos[1] < self.coordinates[1] + self.size[1]

    def change_text_offset(self, offset: tuple):
        self.text_offset = offset

    def change_hover_color(self, color: tuple):
        self.hover_color = color

    def change_color(self, color: tuple):
        self.rect_color = color


class PathfindingGUI:
    EMPTY = 0
    START = 'A'
    END = 'B'
    OBSTACLE = '*'
    PATH = 'X'
    WEIGHTED_PATH = 'Y'
    WEIGHT = 'W'
    SUCCESSOR = 1
    WEIGHTED_SUCCESSOR = 2

    DARK_BLUE = (30, 32, 40)
    BLUE = (85, 180, 217)
    BLUE2 = (52, 94, 112)
    WHITE = (250, 250, 250)
    LIGHT_GRAY = (140, 140, 140)
    GRAY = (100, 100, 100)
    DARK_GRAY = (50, 50, 50)
    GREEN = (81, 138, 45)
    YELLOW = (247, 238, 166)
    DARK_YELLOW = (139, 140, 93)
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
        self.buttons = self.create_buttons()
        self.algorithm = a_star.visual_search

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
                  self.START: self.GREEN, self.END: self.RED, self.PATH: self.BLUE, self.WEIGHT: self.LIGHT_GRAY,
                  self.WEIGHTED_SUCCESSOR: self.DARK_YELLOW, self.WEIGHTED_PATH: self.BLUE2}

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

    def create_buttons(self) -> set:
        """Create the set of buttons; Excludes the 'Draw' buttons."""
        search_button = Button(self.display, (570, 10), (160, 55), self.RED, 'SEARCH', 48, self.WHITE)
        reset_button = Button(self.display, (780, 15), (130, 45), self.WHITE, 'RESET', 40, self.DARK_BLUE)
        reset_button.change_text_offset((0, 2))
        algorithm_button = Button(self.display, (960, 15), (200, 45), self.WHITE, 'ALGORITHM', 40, self.DARK_BLUE)
        algorithm_button.change_text_offset((0, 2))

        return {search_button, reset_button, algorithm_button}

    def draw_buttons(self):
        """Draw the clickable buttons."""
        for button in self.buttons:
            button.draw()

        self.draw_draw_menu()

    def algorithms_menu(self):
        menu_open = True
        shadow = pygame.Surface(self.display.get_size())
        shadow.fill((30, 32, 40))  # Dark blue
        shadow.set_alpha(70)
        self.display.blit(shadow, (0, 0))
        a_star_button = Button(self.display, (960, 60), (200, 45), self.WHITE, 'A* SEARCH', 32, self.DARK_BLUE)
        dijkstra_button = Button(self.display, (960, 105), (200, 45), self.WHITE, "DIJKSTRA'S", 32, self.DARK_BLUE)
        breadth_first_search_button = Button(self.display, (960, 150), (200, 45), self.WHITE, 'BREADTH FIRST SEARCH',
                                             23, self.DARK_BLUE)
        if self.algorithm == a_star.visual_search:
            a_star_button.change_color(self.GRAY)
        elif self.algorithm == dijkstra.visual_search:
            dijkstra_button.change_color(self.GRAY)
        else:
            breadth_first_search_button.change_color(self.GRAY)

        while menu_open:
            mouse_pos = pygame.mouse.get_pos()
            a_star_button.draw()
            dijkstra_button.draw()
            breadth_first_search_button.draw()
            pygame.display.update()

            for event in pygame.event.get():
                if not (960 < mouse_pos[0] < 1160 and 15 < mouse_pos[1] < 195):
                    menu_open = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if a_star_button.is_on():
                        self.algorithm = a_star.visual_search
                        a_star_button.change_color(self.GRAY)
                        dijkstra_button.change_color(self.WHITE)
                        breadth_first_search_button.change_color(self.WHITE)
                    if dijkstra_button.is_on():
                        self.algorithm = dijkstra.visual_search
                        a_star_button.change_color(self.WHITE)
                        dijkstra_button.change_color(self.GRAY)
                        breadth_first_search_button.change_color(self.WHITE)
                    if breadth_first_search_button.is_on():
                        self.algorithm = breadth_first_search.visual_search
                        a_star_button.change_color(self.WHITE)
                        dijkstra_button.change_color(self.WHITE)
                        breadth_first_search_button.change_color(self.GRAY)

    def draw_draw_menu(self):
        """Draw the 'Draw:' section of the buttons.'"""
        modes = [(self.START, 0, self.GREEN, 'START', (0, 0)), (self.END, 1, self.RED, '  END', (2, 0)),
                 (self.WEIGHT, 2, self.LIGHT_GRAY, 'WEIGHT', (-6, 0)), (self.OBSTACLE, 3, self.DARK_GRAY, ' WALL', (0, 0)),
                 (self.EMPTY, 4, self.WHITE, 'ERASE', (-2, 0))]

        title_font = pygame.font.SysFont('freesansbold.ttf', 48)
        button_font = pygame.font.SysFont('freesansbold.ttf', 24)
        self.display.blit(title_font.render('DRAW:', True, self.WHITE), (25, 33))

        mouse_pos = pygame.mouse.get_pos()
        for mode, i, color, title, offset in modes:
            if mode == self.draw_status:
                pygame.draw.rect(self.display, self.GRAY, (157 + (70 * i), 5, 70, 65))
            if 157 + (70 * i) < mouse_pos[0] < 227 + (70 * i) and 5 < mouse_pos[1] < 70:
                pygame.draw.rect(self.display, self.LIGHT_GRAY, (157 + (70 * i), 5, 70, 65))

            pygame.draw.rect(self.display, color, (180 + (70 * i), 15, 25, 25))
            self.display.blit(button_font.render(title, True, self.WHITE), (165 + (70 * i) + offset[0], 48))

    def solve(self):
        """Solve the board visually."""
        if self.paths_exist:
            self.reset()

        self.paths_exist = True
        node = self.algorithm(self)
        self.clock.tick(45)

        if node:
            path = []
            while node.parent is not None:
                node = node.parent
                path.append((node.x, node.y))

            for i in range(len(path) - 1, -1, -1):
                self.clock.tick(15)
                if self.board[path[i][0]][path[i][1]] == self.SUCCESSOR:
                    self.board[path[i][0]][path[i][1]] = self.PATH
                else:
                    self.board[path[i][0]][path[i][1]] = self.WEIGHTED_PATH
                self.draw_grid()
                pygame.display.update()

    def reset(self):
        """Clears the board of paths if paths exist.
        If there are no paths, clear the board of obstacles."""
        x, y = self.board_size
        if self.paths_exist:
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if self.board[row][col] == self.PATH or self.board[row][col] == self.SUCCESSOR:
                        self.board[row][col] = self.EMPTY
                    if self.board[row][col] == self.WEIGHTED_SUCCESSOR or self.board[row][col] == self.WEIGHTED_PATH:
                        self.board[row][col] = self.WEIGHT
            self.paths_exist = False
        else:
            self.board = [[self.EMPTY for _ in range(y)] for _ in range(x)]
        self.set_target_points()

    def mouse_button_down(self, mouse_pos: tuple):
        """Deals with button presses."""
        for i in range(5):
            status = {0: self.START, 1: self.END, 2: self.WEIGHT, 3: self.OBSTACLE, 4: self.EMPTY}
            if 157 + (70 * i) < mouse_pos[0] < 227 + (70 * i) and 5 < mouse_pos[1] < 70:
                self.draw_status = status[i]
        if 570 < mouse_pos[0] < 730 and 10 < mouse_pos[1] < 65:
            self.solve()
        if 780 < mouse_pos[0] < 920 and 15 < mouse_pos[1] < 60:
            self.reset()
        if 26 < mouse_pos[0] < 49 * 26 and 75 < mouse_pos[1] < 75 + 30 * 26:
            self.draw_points()
        if 960 < mouse_pos[0] < 1160 and 15 < mouse_pos[1] < 60:
            self.algorithms_menu()


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
                pathfinding.mouse_button_down(mouse_pos)

        if pygame.mouse.get_pressed()[0]:
            pathfinding.draw_obstacle()

        pygame.display.update()


main()
