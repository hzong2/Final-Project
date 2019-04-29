"""Gomoku Game: Beat the Bot!"""

import sys
import random
import pygame
from pygame.locals import *
import pygame.gfxdraw
from checkerboard import Checkerboard, Black_Piece, White_Piece, offset, Point

size = 30  # Distance between each point on the grid.
num_points = 19  # Number of points on each row/column
outer_width = 20  # Out width of the grid
border_width = 4  # Width of the frame
inside_width = 4  # Distance between the frame and the grid
border_length = size * (num_points - 1) + inside_width * 2 + border_width  # Length of the frame
start_X = start_Y = outer_width + int(border_width / 2) + inside_width  # Starting point of the grid (upper left)
screen_height = size * (num_points - 1) + outer_width * 2 + border_width + inside_width * 2  # Height of game screen
screen_width = screen_height + 200  # Width of game screen

# Radius of a piece
Piece_Radius = size // 2 - 3
Piece_Radius2 = size // 2 + 3

# Color of the grid
Checkerboard_Color = (255, 255, 255)
Indigo_Color = (75, 0, 130)
White_Color = (255, 255, 255)
Red_Color = (200, 30, 30)
Green_Color = (0, 128, 0)

# Right starting point
Right_Init_Pos_X = screen_height + Piece_Radius2 * 2 + 10

# Create the txt screen
def print_msg(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

# Main function that initialize the game
def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Gomoku')

    # Font and font size
    font1 = pygame.font.SysFont('Arial', 35)
    font2 = pygame.font.SysFont('Arial', 65)
    fwidth, fheight = font2.size('Player Wins')

    # Draw the board and initiate the game
    checkerboard = Checkerboard(num_points)
    cur_runner = Black_Piece
    winner = None
    computer = AI(num_points, White_Piece)

    # Counting progress on who is winning
    black_win_count = 0
    white_win_count = 0
    # If the game is not over, then the following iteration goes
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if winner is not None:
                        winner = None
                        cur_runner = Black_Piece
                        checkerboard = Checkerboard(num_points)
                        computer = AI(num_points, White_Piece)
            elif event.type == MOUSEBUTTONDOWN:
                if winner is None:
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        click_point = _get_clickpoint(mouse_pos)
                        if click_point is not None:
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(cur_runner, click_point)
                                if winner is None:
                                    cur_runner = _get_next(cur_runner)
                                    computer.get_opponent_drop(click_point)
                                    AI_point = computer.AI_drop()
                                    winner = checkerboard.drop(cur_runner, AI_point)
                                    if winner is not None:
                                        white_win_count += 1
                                    cur_runner = _get_next(cur_runner)
                                else:
                                    black_win_count += 1
                        else:
                            print('Out of Bound')

        # Draw the grid
        _draw_board(screen)

        # Draw the existing pieces on the grid
        for i, row in enumerate(checkerboard.checkerboard):
            for j, cell in enumerate(row):
                if cell == Black_Piece.Value:
                    _draw_piece(screen, Point(j, i), Black_Piece.Color)
                elif cell == White_Piece.Value:
                    _draw_piece(screen, Point(j, i), White_Piece.Color)

        _draw_left_info(screen, font1, cur_runner, black_win_count, white_win_count)
        # If a winner appears, then print the following txt.
        if winner:
            print_msg(screen, font2, (screen_width - fwidth)//2, (screen_height - fheight)//2, winner.Name + ' Wins', Red_Color)

        pygame.display.flip()

# Determine who goes next
def _get_next(cur_runner):
    if cur_runner == Black_Piece:
        return White_Piece
    else:
        return Black_Piece


# Draw the board (grid)
def _draw_board(screen):
    # Fill the background color of the board
    screen.fill(Checkerboard_Color)
    # Draw the frame lines
    pygame.draw.rect(screen, Indigo_Color, (outer_width, outer_width, border_length, border_length), border_width)
    # Draw the grid
    for i in range(num_points):
        pygame.draw.line(screen, Indigo_Color,
                         (start_Y, start_Y + size * i),
                         (start_Y + size * (num_points - 1), start_Y + size * i),
                         1)
    for j in range(num_points):
        pygame.draw.line(screen, Indigo_Color,
                         (start_X + size * j, start_X),
                         (start_X + size * j, start_X + size * (num_points - 1)),
                         1)
    # Draw the four corner centers and the very center
    for i in (3, 9, 15):
        for j in (3, 9, 15):
            if i == j == 9:
                radius = 5
            else:
                radius = 3
            # pygame.draw.circle(screen, BLACK, (Start_X + SIZE * i, Start_Y + SIZE * j), radius)
            pygame.gfxdraw.aacircle(screen, start_X + size * i, start_Y + size * j, radius, Indigo_Color)
            pygame.gfxdraw.filled_circle(screen, start_X + size * i, start_Y + size * j, radius, Indigo_Color)




# Show the left-hand-side information
def _draw_left_info(screen, font, cur_runner, black_win_count, white_win_count):
    _draw_piece_pos(screen, (screen_height + Piece_Radius2, start_X + Piece_Radius2), Black_Piece.Color)
    _draw_piece_pos(screen, (screen_height + Piece_Radius2, start_X + Piece_Radius2 * 4), White_Piece.Color)

    print_msg(screen, font, Right_Init_Pos_X, start_X + 3, 'Player', Green_Color)
    print_msg(screen, font, Right_Init_Pos_X, start_X + Piece_Radius2 * 3 + 3, 'Bot', Green_Color)

    print_msg(screen, font, screen_height, screen_height - Piece_Radius2 * 8, 'Progress:', Green_Color)
    _draw_piece_pos(screen, (screen_height + Piece_Radius2, screen_height - int(Piece_Radius2 * 4.5)), Black_Piece.Color)
    _draw_piece_pos(screen, (screen_height + Piece_Radius2, screen_height - Piece_Radius2 * 2), White_Piece.Color)
    print_msg(screen, font, Right_Init_Pos_X, screen_height - int(Piece_Radius2 * 5.5) + 3, f'{black_win_count} Wins', Green_Color)
    print_msg(screen, font, Right_Init_Pos_X, screen_height - Piece_Radius2 * 3 + 3, f'{white_win_count} Wins', Green_Color)

# Draw the piece
def _draw_piece(screen, point, stone_color):
    # pygame.draw.circle(screen, stone_color, (Start_X + SIZE * point.X, Start_Y + SIZE * point.Y), Stone_Radius)
    pygame.gfxdraw.aacircle(screen, start_X + size * point.X, start_Y + size* point.Y, Piece_Radius, stone_color)
    pygame.gfxdraw.filled_circle(screen, start_X + size * point.X, start_Y + size * point.Y, Piece_Radius, stone_color)

# Draw the piece position
def _draw_piece_pos(screen, pos, stone_color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Piece_Radius2, stone_color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Piece_Radius2, stone_color)


# Return to the game coordinate based on the location of the mouse pointer
def _get_clickpoint(click_pos):
    pos_x = click_pos[0] - start_X
    pos_y = click_pos[1] - start_Y
    if pos_x < -inside_width or pos_y < -inside_width:
        return None
    x = pos_x // size
    y = pos_y // size
    if pos_x % size > Piece_Radius:
        x += 1
    if pos_y % size > Piece_Radius:
        y += 1
    if x >= num_points or y >= num_points:
        return None

    return Point(x, y)


class AI:
    def __init__(self, line_points, chessman):
        self._line_points = line_points
        self._my = chessman
        self._opponent = Black_Piece if chessman == White_Piece else White_Piece
        self._checkerboard = [[0] * line_points for _ in range(line_points)]

    def get_opponent_drop(self, point):
        self._checkerboard[point.Y][point.X] = self._opponent.Value

    def AI_drop(self):
        point = None
        score = 0
        for i in range(self._line_points):
            for j in range(self._line_points):
                if self._checkerboard[j][i] == 0:
                    _score = self._get_point_score(Point(i, j))
                    if _score > score:
                        score = _score
                        point = Point(i, j)
                    elif _score == score and _score > 0:
                        r = random.randint(0, 100)
                        if r % 2 == 0:
                            point = Point(i, j)
        self._checkerboard[point.Y][point.X] = self._my.Value
        return point

    def _get_point_score(self, point):
        score = 0
        for os in offset:
            score += self._get_direction_score(point, os[0], os[1])
        return score

    def _get_direction_score(self, point, x_offset, y_offset):
        count = 0   # Count the consecutive pieces of BOT
        _count = 0  # Count the consecutive pieces of Player
        space = None   # Check if there is space between consecutive pieces of BOT
        _space = None  # Check if there is space between consecutive pieces of Player
        both = 0    # Check blocking between consecutive pieces of BOT
        _both = 0   # Check blocking between consecutive pieces of Player

        # 1 for BOT, 2 for Player
        flag = self._get_piece_color(point, x_offset, y_offset, True)
        if flag != 0:
            for step in range(1, 6):
                x = point.X + step * x_offset
                y = point.Y + step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break   # exit at 2nd space
                    elif flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # Side dropping counts as blocking
                    if flag == 1:
                        both += 1
                    elif flag == 2:
                        _both += 1

        if space is False:
            space = None
        if _space is False:
            _space = None

        _flag = self._get_piece_color(point, -x_offset, -y_offset, True)
        if _flag != 0:
            for step in range(1, 6):
                x = point.X - step * x_offset
                y = point.Y - step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if _flag == 1:
                        if self._checkerboard[y][x] == self._my.Value:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break   # exit at 2nd space
                    elif _flag == 2:
                        if self._checkerboard[y][x] == self._my.Value:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._opponent.Value:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # Side dropping counts as blocking
                    if _flag == 1:
                        both += 1
                    elif _flag == 2:
                        _both += 1

        score = 0
        if count == 4:
            score = 10000
        elif _count == 4:
            score = 9000
        elif count == 3:
            if both == 0:
                score = 1000
            elif both == 1:
                score = 100
            else:
                score = 0
        elif _count == 3:
            if _both == 0:
                score = 900
            elif _both == 1:
                score = 90
            else:
                score = 0
        elif count == 2:
            if both == 0:
                score = 100
            elif both == 1:
                score = 10
            else:
                score = 0
        elif _count == 2:
            if _both == 0:
                score = 90
            elif _both == 1:
                score = 9
            else:
                score = 0
        elif count == 1:
            score = 10
        elif _count == 1:
            score = 9
        else:
            score = 0

        if space or _space:
            score /= 2

        return score

    # Make sure there is no overlapping of pieces
    def _get_piece_color(self, point, x_offset, y_offset, next):
        x = point.X + x_offset
        y = point.Y + y_offset
        if 0 <= x < self._line_points and 0 <= y < self._line_points:
            if self._checkerboard[y][x] == self._my.Value:
                return 1
            elif self._checkerboard[y][x] == self._opponent.Value:
                return 2
            else:
                if next:
                    return self._get_piece_color(Point(x, y), x_offset, y_offset, False)
                else:
                    return 0
        else:
            return 0


if __name__ == '__main__':
    main()
