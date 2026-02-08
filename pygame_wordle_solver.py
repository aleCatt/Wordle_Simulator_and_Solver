import pygame # type: ignore (To hide Pylance(reportMissingimports))
from sys import exit
from wordle_utils import (load_words, filter_solutions, get_score,
                          POSSIBLE_SOLUTIONS_PATH, ALLOWED_GUESSES_PATH)

COLORS = {'BACKGROUND': '#191919','TEXT': '#F8F8F8', 'DEFAULT': "#6B7280", # Button edges & Letter outlines
          'GRAY': '#3A3A3C','YELLOW': '#DBC03D', 'GREEN': '#538D4E', 'RED': "#E23636", 'BLUE': "#1D409A"}
WIDTH = 1000
HEIGHT = 1000

def get_suggestion(suggestion: str, pattern: tuple[int]) -> str:
    global guessed, correct_positions, known_letters, possible_solutions, allowed
    
    # Update learned information from the guess we just made
    guessed.append(suggestion)
    for i, (letter, color) in enumerate(zip(suggestion, pattern)):
        if color == 2:  # Green
            correct_positions[i] = letter
            known_letters.add(letter)
        elif color == 1:  # Yellow
            known_letters.add(letter)

    # Filter possible solutions based on feedback
    possible_solutions = filter_solutions(suggestion, pattern, possible_solutions)
    print(f'Remaining solutions: {len(possible_solutions)}')

    suggestion: str = ''
    # Check if we have no valid solutions left (likely a feedback error)
    if len(possible_solutions) == 0:
        print('No valid solutions remaining! Please check your feedback patterns.')
    # If we're down to very few solutions, just pick one
    elif len(possible_solutions) <= 2:
        suggestion = possible_solutions[0]
    # Otherwise, calculate the best next guess
    else:
        best_score: float = -float('inf')
        for word in allowed:
            if word in guessed: continue
            score: float = get_score(word, possible_solutions, known_letters, correct_positions)
            if score > best_score:
                best_score = score
                suggestion = word
    return suggestion

class Letter:
    def __init__(self,
                 char: str = '*',
                 width: int = 180, height: int = 180,
                 pos: tuple[int, int] = (0, 0)) -> None:
        self.color = COLORS['DEFAULT']
        self.bg_rect = pygame.Rect(pos, (width, height))
        self.text_surf = gui_font.render(char, True, COLORS['TEXT'])
        self.text_rect = self.text_surf.get_rect(center = self.bg_rect.center)

    def draw(self):
        if self.color == COLORS['DEFAULT']: # only the outline
            pygame.draw.rect(window, self.color, self.bg_rect, border_radius = 12, width = 4)
        else:
            pygame.draw.rect(window, self.color, self.bg_rect, border_radius = 12)
        window.blit(self.text_surf, self.text_rect)

    def change_color(self, new_color: str = COLORS['DEFAULT']) -> None:
        self.color = new_color
    def change_char(self, new_char: str) -> None:
        self.text_surf = gui_font.render(new_char, True, COLORS['TEXT'])

class Button:
    def __init__(self, 
                 text: str = '', top_color: str = '#000000',
                 width: int = 288, height: int = 288,
                 pos: tuple[int, int] = (0, 0),
                 elevation: int = 6) -> None:
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color

        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = COLORS['DEFAULT']

        # Text
        self.text_surf = gui_font.render(text, True, COLORS['TEXT'])
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self) -> None:
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(window, self.bottom_color, self.bottom_rect, border_radius = 12)
        pygame.draw.rect(window, self.top_color, self.top_rect, border_radius = 12)
        window.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            elif self.pressed == True:
                self.dynamic_elevation = self.elevation
                self.pressed = False
                # click logic
                update_pattern(self.top_color)

def update_pattern(color: str) -> None:
    global pattern_list, letters, pattern

    lenght = len(pattern_list)
    if color == COLORS['RED']: # DEL
        if lenght: # != 0
            pattern_list.pop()
            letters[lenght-1].change_color() # default color
    if lenght != 5:
        if color == COLORS['GRAY']:
            pattern_list.append(0)
            letters[lenght].change_color(COLORS['GRAY'])
        elif color == COLORS['YELLOW']:
            pattern_list.append(1)
            letters[lenght].change_color(COLORS['YELLOW'])
        elif color == COLORS['GREEN']:
            pattern_list.append(2)
            letters[lenght].change_color(COLORS['GREEN'])
    else:
        if color == COLORS['BLUE']: # Enter
            print(f'entered {pattern_list}')
            pattern = tuple(pattern_list)
            pattern_list = []

def reset_letters(word: str) -> None:
    global letters
    for i in range(5):
        letters[i].change_char(word[i])
        letters[i].change_color() # default color

if __name__ == '__main__':

    # Only possible solutions
    possible_solutions: list[str] = load_words(POSSIBLE_SOLUTIONS_PATH)
    # All allowed words
    allowed: list[str] = load_words(ALLOWED_GUESSES_PATH)

    # Track learned information
    guessed: list[str] = []  # Words we've already guessed
    known_letters: set[str] = set()  # Letters we know are in the word
    correct_positions: dict[int, str] = {} # position: letter

    # Initial guess, good ones: 'soare', 'salet', 'trace'
    suggestion: str = 'raise'

    pattern_list = []
    pattern = tuple()

    # Pygame setup
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Wordle Solver')
    clock = pygame.time.Clock() # for framerate
    gui_font = pygame.font.Font(None, 100)

    # Word
    letter0 = Letter(pos = (50, 50))
    letter1 = Letter(pos = (230, 50))
    letter2 = Letter(pos = (410, 50))
    letter3 = Letter(pos = (590, 50))
    letter4 = Letter(pos = (770, 50))

    letters = [letter0, letter1, letter2, letter3, letter4]
    reset_letters(suggestion)

    # Buttons
    gray_button = Button(pos = (50, 356), top_color = COLORS['GRAY'])
    yellow_button = Button(pos = (356, 356), top_color = COLORS['YELLOW'])
    green_button = Button(pos = (662, 356), top_color = COLORS['GREEN'])
    delete_button = Button(text = 'DEL', width = 441, pos = (50, 662), top_color = COLORS['RED'])
    enter_button = Button(text = 'Enter', width = 441, pos = (509, 662), top_color = COLORS['BLUE'])

    buttons = [gray_button, yellow_button, green_button, delete_button, enter_button]

    # Game loop
    while True:

        for event in pygame.event.get():
            # X button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        window.fill(COLORS['BACKGROUND'])
        for letter in letters:
            letter.draw()
        for button in buttons:
            button.draw()

        if pattern: # is submitted
            if pattern == (2, 2, 2, 2, 2):
                print('Solved!')
                pygame.quit()
                exit()
            suggestion = get_suggestion(suggestion, pattern)
            if not suggestion: # no valid answer
                pygame.quit()
                exit()
            reset_letters(suggestion)
            pattern_list = []
            pattern = tuple()

        pygame.display.update()
        clock.tick(60) # 60 fps