import pygame # type: ignore (To hide Pylance(reportMissingimports))
from sys import exit
from wordle_utils import WordleSolver
                          
COLORS: dict[str, str] = {'BACKGROUND': '#191919','TEXT': '#F8F8F8', 
                          'DEFAULT': "#6B7280", # Button edges & Letter outlines
                          'GRAY': '#3A3A3C','YELLOW': '#DBC03D', 'GREEN': '#538D4E', 
                          'RED': "#E23636", 'BLUE': "#1D409A"}
COLOR2INT: dict[str, int] = {COLORS['GRAY']: 0, COLORS['YELLOW']: 1, COLORS['GREEN']: 2}
KEY2COLOR: dict[int, str] = {pygame.K_0 : COLORS['GRAY'], pygame.K_1: COLORS['YELLOW'], pygame.K_2: COLORS['GREEN'], pygame.K_BACKSPACE: COLORS['RED'], pygame.K_RETURN: COLORS['BLUE']}

WINDOW_SIZE: tuple[int, int] = (1000, 1000)
MARGIN_SIZE: int = 50
BUTTON_SPACING: int = 18 # Space between buttons (both vertical and horizontal)

LETTER_SIZE: int = (WINDOW_SIZE[0] - 2 * MARGIN_SIZE) // 5
BUTTON_SIZE: int = (WINDOW_SIZE[0] - 2 * MARGIN_SIZE - 2 * BUTTON_SPACING) // 3
WIDE_BUTTON_WIDTH: int = (WINDOW_SIZE[0] - 2 * MARGIN_SIZE - BUTTON_SPACING) // 2
# Space between letters and buttons
VERTICAL_SPACING = WINDOW_SIZE[1] - 2 * MARGIN_SIZE - LETTER_SIZE - BUTTON_SPACING - 2 * BUTTON_SIZE

class Letter:
    def __init__(self, window: pygame.Surface, font: pygame.Font,
                 char: str = '*',
                 size: tuple[int, int] = (LETTER_SIZE, LETTER_SIZE),
                 pos: tuple[int, int] = (0, 0)) -> None:
        self.window = window
        self.font = font
        self.bg_rect = pygame.Rect(pos, size)
        self.text_surf = self.font.render(char, True, COLORS['TEXT'])
        self.text_rect = self.text_surf.get_rect(center = self.bg_rect.center)

    def draw(self, color: str = COLORS['DEFAULT']) -> None:
        if color == COLORS['DEFAULT']: # only the outline
            pygame.draw.rect(self.window, color, self.bg_rect, border_radius = 12, width = 4)
        else:
            pygame.draw.rect(self.window, color, self.bg_rect, border_radius = 12)
        self.window.blit(self.text_surf, self.text_rect)

    def change_char(self, new_char: str) -> None:
        self.text_surf = self.font.render(new_char, True, COLORS['TEXT'])

class Button:
    def __init__(self, window: pygame.Surface, font: pygame.Font,
                 text: str = '', top_color: str = '#000000',
                 size: tuple[int, int] = (BUTTON_SIZE, BUTTON_SIZE),
                 pos: tuple[int, int] = (0, 0),
                 elevation: int = 6) -> None:
        # Core attributes
        self.window = window
        self.font = font
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos, size)
        self.top_color = top_color

        self.bottom_rect = pygame.Rect(pos, (size[0], elevation))
        self.bottom_color = COLORS['DEFAULT']

        # Text
        self.text_surf = self.font.render(text, True, COLORS['TEXT'])
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self) -> None:
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.window, self.bottom_color, self.bottom_rect, border_radius = 12)
        pygame.draw.rect(self.window, self.top_color, self.top_rect, border_radius = 12)
        self.window.blit(self.text_surf, self.text_rect)

    def is_clicked(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            elif self.pressed == True:
                self.dynamic_elevation = self.elevation
                self.pressed = False
                return True
        return False

def quit() -> None:
    pygame.quit()
    exit()

def update_pattern(action: str, pattern: list[str]) -> tuple[list[str], bool]:
    submit = False
    lenght = len(pattern)
    if action == COLORS['RED']: # DEL
        if lenght: # != 0
            pattern.pop()
    elif action == COLORS['BLUE']: # Enter
        if lenght == 5:
            submit = True 
    elif lenght != 5:
        pattern.append(action)       
    return pattern, submit

def draw_letters(letters: list[Letter], pattern: list[str]) -> None:
    lenght = len(pattern)
    for i in range(lenght):
        letters[i].draw(pattern[i])
    for i in range(lenght, 5):
        letters[i].draw()

def draw_buttons(buttons: list[Button]) -> None:
    for button in buttons:
        button.draw()

def reset_letters(word: str, letters: list[Letter]) -> None:
    for i in range(5):
        letters[i].change_char(word[i])

def handle_events(buttons) -> str:
    action = None
    for event in pygame.event.get():
        # X button -> quit
        if event.type == pygame.QUIT:
            quit()
        # key press logic
        if event.type == pygame.KEYDOWN:
            key = event.key
            # escape -> quit
            if key == pygame.K_ESCAPE:
                quit()
            elif key in KEY2COLOR:
                action = KEY2COLOR[key]
    for button in buttons:
        if button.is_clicked():
            action = button.top_color
    return action

def main() -> None:

    solver = WordleSolver()

    pattern_list: list[int] = []
    is_submitted: bool = False

    # Pygame setup
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Wordle Solver')
    clock = pygame.time.Clock() # for framerate
    gui_font = pygame.font.Font(None, 100)

    letters = [
        Letter(window = window, font = gui_font, pos = (MARGIN_SIZE, MARGIN_SIZE)),
        Letter(window = window, font = gui_font, pos = (MARGIN_SIZE + LETTER_SIZE, MARGIN_SIZE)),
        Letter(window = window, font = gui_font, pos = (MARGIN_SIZE + 2 * LETTER_SIZE, MARGIN_SIZE)),
        Letter(window = window, font = gui_font, pos = (MARGIN_SIZE + 3 * LETTER_SIZE, MARGIN_SIZE)),
        Letter(window = window, font = gui_font, pos = (MARGIN_SIZE + 4 * LETTER_SIZE, MARGIN_SIZE))
        ]

    reset_letters(solver.suggestion, letters)

    buttons = [
        # Gray
        Button(window = window, font = gui_font, top_color = COLORS['GRAY'],
                pos = (MARGIN_SIZE, MARGIN_SIZE + LETTER_SIZE + VERTICAL_SPACING)),
        # Yellow
        Button(window = window, font = gui_font, top_color = COLORS['YELLOW'],
                pos = (MARGIN_SIZE + BUTTON_SPACING + BUTTON_SIZE, MARGIN_SIZE + LETTER_SIZE + VERTICAL_SPACING)),
        # Green
        Button(window = window, font = gui_font, top_color = COLORS['GREEN'],
                pos = (MARGIN_SIZE + 2 * BUTTON_SPACING + 2 * BUTTON_SIZE, MARGIN_SIZE + LETTER_SIZE + VERTICAL_SPACING)),
        # Delete
        Button(window = window, font = gui_font, text = 'DEL', size = (WIDE_BUTTON_WIDTH, BUTTON_SIZE), top_color = COLORS['RED'],
                pos = (MARGIN_SIZE, MARGIN_SIZE + LETTER_SIZE + VERTICAL_SPACING + BUTTON_SIZE + BUTTON_SPACING)),
        # Enter
        Button(window = window, font = gui_font, text = 'Enter', size = (WIDE_BUTTON_WIDTH, BUTTON_SIZE), top_color = COLORS['BLUE'],
                pos = (MARGIN_SIZE + BUTTON_SPACING + WIDE_BUTTON_WIDTH, MARGIN_SIZE + LETTER_SIZE + VERTICAL_SPACING + BUTTON_SIZE + BUTTON_SPACING))
        ]
    
    # Game loop
    while True:

        action = handle_events(buttons)
        if action:
            pattern_list, is_submitted = update_pattern(action, pattern_list)
        if is_submitted:
            pattern = tuple([COLOR2INT[c] for c in pattern_list])
            if pattern == (2, 2, 2, 2, 2):
                print('[DEBUG] Solved!')
                quit()
            solver.process_feedback(pattern)
            reset_letters(solver.suggestion, letters)
            pattern_list = []
            is_submitted = False

        window.fill(COLORS['BACKGROUND'])
        draw_letters(letters, pattern_list)
        draw_buttons(buttons)
        pygame.display.update()
        clock.tick(60) # 60 fps

if __name__ == '__main__':
    main()