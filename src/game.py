import pygame
import sys
import math
import random
import time

from enum import Enum
from variables import ROW_COUNT, COLUMN_COUNT, SQUARESIZE, size, RADIUS, colors, height, width, PLAYER, AI, \
    PLAYER_PIECE, AI_PIECE, thinking_time, game_end_button_width, game_end_button_height, level_button_height, \
    level_button_width
from functions import create_board, is_valid_location, get_next_open_row, drop_piece, game_over_check, draw_board, \
    board, screen, draw_dotted_circle
from score_ai import pick_best_move
from minmax_ai import minimax
from ui_components import Button
from ui_components import ai_move_sound, self_move_sound, ai_wins_sound, player_wins_sound

class Difficulty(Enum):
    EASY = 1
    INTERMEDIATE = 2
    HARD = 3
    IMPOSSIBLE = 4
    GODMODE = 5

class ConnectFour:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() #added to initialize sound
        self.game_over = False
        self.turn = None  # Removed random selection of first turn
        self.board = create_board()
        self.myfont = pygame.font.SysFont("monospace", 80)
        padding = 20
        restart_button_y = height // 2
        quit_button_y = restart_button_y + game_end_button_height + padding
        self.center_x = width // 2 - game_end_button_width // 2
        self.quit_button = Button(colors["RED"], self.center_x, quit_button_y, game_end_button_width,
                                  game_end_button_height, 'Quit')
        self.restart_button = Button(colors["GREEN"], self.center_x, restart_button_y,
                                     game_end_button_width, game_end_button_height,
                                     'Restart')
        pygame.display.set_caption("Connect Four")
        self.opponent = self.choose_opponent()  # Added opponent selection
        print(self.opponent)
        if self.opponent == "AI":
            self.difficulty = self.choose_difficulty()
            self.turn = PLAYER
        elif self.opponent == "AI vs AI":#/////
            self.difficulty = Difficulty.HARD # Difficulty for AI VS AI 
            self.turn = AI#/////
        else:
            self.turn = PLAYER
        self.first = True
        screen.fill(colors["DARKGREY"])
        draw_board(self.board)
        pygame.display.update()


#mouse motion depends as to how the mouse moves
    def handle_mouse_motion(self, event):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE)) #remove the dotted circle
        posx = event.pos[0]
        if self.turn == PLAYER:
            draw_dotted_circle(screen, posx, int(SQUARESIZE / 2), RADIUS, colors["YELLOW"], gap_length=6)
        pygame.display.update()

#mouse button right - click
    def handle_mouse_button_down(self, event):
        if(self.opponent == "Player"): #player vs player
            if self.first:
                p = AI_PIECE #not ai but for player 1 turn
            else:
                p = PLAYER_PIECE
        else:
            p = PLAYER_PIECE
        #pygame.draw.rect(screen, colors, (0, 0, width, SQUARESIZE))
        posx = event.pos[0]
        if (self.turn == PLAYER and self.opponent == "AI") or self.opponent == "Player": #player vs player or player vs ai with player as the first turn
            col = int(math.floor(posx / SQUARESIZE)) #selcting column based on x coordinate
            if is_valid_location(self.board, col): 
                self_move_sound.play()
                self._extracted_from_ai_move_7(col, p, "Player " + str(self.turn)+" wins!") #which row is empty you have selected and which cloumn is empty
                self_move_sound.play()
                self.turn ^= 1 #changing 1 to 0 and vice versa
                self.first = not self.first
                if self.opponent == "Player":
                    self.render_thinking("Player #" + str(self.turn)+ " Turn")
                else:
                    self.render_thinking("Thinking...")
                draw_board(self.board)
        if self.game_over:
            if self.quit_button.is_over((posx, event.pos[1])):
                sys.exit()
            elif self.restart_button.is_over((posx, event.pos[1])):
                self.__init__()


    def ai_move(self):
        thinking_time = 1 #for delay
        if self.opponent == "AI": #if player vs ai
            player = AI_PIECE #ai piece 2 and player piece 1
        elif self.opponent == "AI vs AI":#/////
            player = self.turn + 1 #selfturn can be 1 and 0 board has values 1 and 2 to match board values 
        if self.difficulty == Difficulty.EASY:
            col = random.randint(0, COLUMN_COUNT-1)
            time.sleep(thinking_time + 1)
        if self.difficulty == Difficulty.INTERMEDIATE:
            col = pick_best_move(self.board,
                                player,
                                directions=tuple(1 if i in random.sample(range(4), 2) else 0 for i in range(4)))
            time.sleep(thinking_time + 1.2)
        if self.difficulty == Difficulty.HARD:
            #col = pick_best_move(self.board, player)
            col, minimaxScore = minimax(self.board, 4, -math.inf, math.inf, True)
            time.sleep(thinking_time + 1.5)

        if self.difficulty == Difficulty.IMPOSSIBLE:
            col, minimaxScore = minimax(self.board, 6, -math.inf, math.inf, True)
        if self.difficulty == Difficulty.GODMODE:
            col, minimaxScore = minimax(self.board, 7, -math.inf, math.inf, True)
        if is_valid_location(self.board, col):
            ai_move_sound.play()
            self._extracted_from_ai_move_7(col, player, "AI wins!! :[")
            self.turn ^= 1 #chamging turn

    # plays move for ai and player both
    # TODO Rename this here and in `handle_mouse_button_down` and `ai_move`
    def _extracted_from_ai_move_7(self, col, arg1, arg2):
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, arg1)
        draw_board(self.board)
        pygame.display.update()
        if game_over_check(self.board, arg1): 
            self.display_winner(arg2)
            self.game_over = True
            return self.handle_game_over()

    def display_winner(self, message):
        if message == "AI wins!! :[":
            ai_wins_sound.play()
        elif message == "You win!! ^_^":
            player_wins_sound.play()
        label = self.myfont.render(message, 1, colors["YELLOW"])
        screen.blit(label, (40, 10))
        pygame.display.update()

    #restart and quit buttons in the end check all game over condition
    def handle_game_over(self):
        #self.clear_label()
        draw_board(self.board)
        self.quit_button.draw(screen, outline_color=colors["DARKGREY"])
        self.restart_button.draw(screen, outline_color=colors["DARKGREY"])
        pygame.display.update()
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.quit_button.is_over((posx, posy)):
                        sys.exit()
                    elif self.restart_button.is_over((posx, posy)):
                        self.__init__()
                        return self.game_start()

            pygame.display.update()


    def choose_difficulty(self):
        btn_height = 90
        text_color = colors['DARKGREY']
        btn_y = [i * (btn_height + 20) + height/1.8 for i in range(-3,3)]
        self.easy = Button(colors['GREEN'], self.center_x,
                           btn_y[0], 250, btn_height,
                           'EASY',
                           text_color=text_color)
        self.intermediate = Button(colors['GREEN'], self.center_x,
                            btn_y[1], 250, btn_height,
                            'INTERMEDIATE',
                            text_color=text_color)

        self.hard = Button(colors['YELLOW'], self.center_x,
                           btn_y[2], 250, btn_height,
                           'HARD',
                           text_color=text_color)
        self.impossible = Button(colors['YELLOW'], self.center_x,
                                 btn_y[3], 250, btn_height,
                                 'IMPOSSIBLE',
                                 text_color=text_color)
        self.godmode = Button(colors['RED'], self.center_x,
                              btn_y[4], 250, btn_height,
                              'GODMODE',
                                text_color=text_color)

        screen.fill(colors['GREY'])
        self.easy.draw(screen)
        self.intermediate.draw(screen)
        self.hard.draw(screen)
        self.impossible.draw(screen)
        self.godmode.draw(screen)

        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.easy.is_over((posx, posy)):
                        return Difficulty.EASY
                    elif self.intermediate.is_over((posx, posy)):
                        return Difficulty.INTERMEDIATE
                    elif self.hard.is_over((posx, posy)):
                        return Difficulty.HARD
                    elif self.impossible.is_over((posx, posy)):
                        return Difficulty.IMPOSSIBLE
                    elif self.godmode.is_over((posx, posy)):
                        return Difficulty.GODMODE

    def choose_opponent(self):
        btn_height = 90
        text_color = colors['DARKGREY']
        btn_y = [i * (btn_height + 20) + height/1.8 for i in range(-2, 2)]  # Adjusted button positions
        self.player = Button(colors['GREEN'], self.center_x,
                             btn_y[0], 250, btn_height,
                             'Player',
                             text_color=text_color)
        self.ai = Button(colors['YELLOW'], self.center_x,
                         btn_y[1], 250, btn_height,
                         'AI',
                         text_color=text_color)
        self.aivsai = Button(colors['RED'], self.center_x,
                         btn_y[2], 250, btn_height,
                         'AI vs AI',
                         text_color=text_color)
        screen.fill(colors['GREY'])
        self.player.draw(screen)
        self.ai.draw(screen)
        self.aivsai.draw(screen)
        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.player.is_over((posx, posy)):
                        return "Player"
                    elif self.ai.is_over((posx, posy)):
                        return "AI"
                    elif self.aivsai.is_over((posx, posy)):
                        return "AI vs AI"
                    
    #for starting the game 
    def game_start(self):
        current_player = PLAYER  # Set the current player to PLAYER at the start of the game
        while not self.game_over: #while game not over
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #cross on the top right 
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
            if self.opponent == "AI" and self.turn == AI and not self.game_over:  # Only AI makes a move if AI is selected as opponent
                    self.ai_move() #for ai turn
                    self.turn = PLAYER #then player turn 
            elif self.opponent == "AI vs AI":  # AI vs AI mode
                #self.first = not self.first
                if (self.turn == 1):
                    self.render_thinking("AI 1 is thinking...")
                else:
                    self.render_thinking("AI 2 is thinking...")    
                self.ai_move()

    # def AIVsAI(self):

                

    def clear_label(self):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))


    def render_thinking(self, text):
        self.clear_label()
        label = pygame.font.SysFont("monospace", 60).render(text, 1, colors["YELLOW"])
        screen.blit(label, (40, 10))
        pygame.display.update()

if __name__ == "__main__":
    game = ConnectFour()
    game.game_start()


# TODO Complete the game and make a downloadable file for the game. Use pybag to take the game to the web.
