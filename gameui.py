import sys
import pygame
import ai
import puzzle


class GameUI:
    def __init__(self, size):
        self.colors = {}
        self.size = size
        self.width = self.height = (size + 1) * 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.init()
        pygame.display.set_caption(self.get_header())
        self.font = pygame.font.SysFont("Arial", 72)
        self.init_colors()
        self.ai = ai.AI(size)
        self.ai_move_index = 0
        self.ai_moves = []
        self.clock = pygame.time.Clock()
        self.in_search = False

    def start(self):
        p = puzzle.Puzzle(self.size)
        while True:
            for event in pygame.event.get():
                self.handle_event(event, p)

            self.draw_puzzle(p)
            pygame.display.flip()
            self.clock.tick(30)

    def handle_event(self, event, p):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                p.shuffle()
                self.ai_move_index = 0
                self.ai_moves = []
                pygame.display.set_caption(self.get_header())

            elif event.key == pygame.K_f:
                if len(self.ai_moves) == 0 and not self.in_search:
                    pygame.display.set_caption(self.get_header("wait..."))
                    self.ai_moves = self.ai.ida_star(p)
                    for event in pygame.event.get():
                        pass
                    self.in_search = False
                    pygame.display.set_caption(self.get_header("found solution"))
                    self.ai_move_index = 0
                else:
                    p.move_blank(self.ai_moves[self.ai_move_index])
                    if p.goal_test():
                        self.ai_move_index = 0
                        self.ai_moves = []
                    else:
                        self.ai_move_index += 1

        elif event.type == pygame.MOUSEBUTTONUP:
            pygame.display.set_caption(self.get_header())
            pos = pygame.mouse.get_pos()
            puzzle_coord = (pos[1] * p.size // self.height,
                            pos[0] * p.size // self.width)
            direction = (puzzle_coord[0] - p.blankTile[0],
                         puzzle_coord[1] - p.blankTile[1])
            self.ai_moves = []
            self.ai_move_index = 0
            if direction == p.RIGHT:
                p.move_blank(p.RIGHT)
            elif direction == p.LEFT:
                p.move_blank(p.LEFT)
            elif direction == p.DOWN:
                p.move_blank(p.DOWN)
            elif direction == p.UP:
                p.move_blank(p.UP)

    def draw_puzzle(self, p):
        self.screen.fill(self.colors["black"])

        for i in range(p.size):
            for j in range(p.size):
                tile_color = self.colors["tile_color"]
                tile_number = str(p[i][j])

                if p[i][j] == 0:
                    tile_color = self.colors["border_color"]
                    tile_number = ''

                rect = pygame.Rect(j * self.width / p.size,
                                   i * self.height / p.size,
                                   self.width / p.size,
                                   self.height / p.size)

                pygame.draw.rect(self.screen, tile_color, rect)
                pygame.draw.rect(self.screen, self.colors["border_color"], rect, 1)

                number_object = self.font.render(tile_number, 1, self.colors["black"])
                self.screen.blit(number_object,
                                 (j * self.width / p.size + (self.width / p.size - number_object.get_width()) / 2,
                                  i * self.height / p.size + (
                                              self.height / p.size - number_object.get_height()) / 2))

    def init_colors(self):
        self.colors = {
            'black': (0, 0, 0),
            "border_color": (92, 90, 86),
            "tile_color": (242, 197, 133)
        }

    def get_header(self, content=""):
        if content != "":
            content = f" | {content}"

        return f"{self.size} puzzle game by Behrang Shirdel {content}"

