# Author: Albert Cheng
# Date: 9-5-2021
# Description: This program provides code for a game called Kuba. Game information and instructions
#              can be found here - https://sites.google.com/site/boardandpieces/list-of-games/kuba

import pygame, sys

pygame.font.init()
message_font = pygame.font.SysFont('Arial', 15)
instruction_font = pygame.font.SysFont('Arial', 20)
pygame.font.Font.set_underline(instruction_font, True)


class PyGameFeatures:
    """
    Represents Kuba game interface using Pygame module
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BEIGE = (244, 226, 198)
    CIRCLE_WIDTH = 60
    BORDER_WIDTH = 5
    CIRCLE_RADIUS = 30
    BOARD_SIDE_LENGTH = 700
    BOARD_START_Y = 50
    BOARD_START_X = 100
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 900

    def __init__(self, my_board, player_1, player_2):
        """
        initializes pygame instance, display,
        """
        # color constants

        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Albert's Kuba Game")
        self.screen.fill(self.BEIGE)

        # draw grid lines
        for i in range(0, 8):
            pygame.draw.line(self.screen, self.BLACK, ((i + 1) * 100, self.BOARD_START_Y),
                             ((i + 1) * 100, 700 + self.BOARD_START_Y), 2)
            pygame.draw.line(self.screen, self.BLACK, (self.BOARD_START_X, i * 100 + self.BOARD_START_Y),
                             (700 + self.BOARD_START_X, i * 100 + self.BOARD_START_Y), 2)
            grid_num = message_font.render(str(i), False, (0, 0, 0))
            if i < 7:
                self.screen.blit(grid_num, (75, i * 100 + 45 + self.BOARD_START_Y))
                self.screen.blit(grid_num, ((i + 1) * 100 + 45, self.BOARD_START_Y - 30))

        for row_num, row in enumerate(my_board):
            for col_num, marble in enumerate(row):
                if marble == 'W':
                    pygame.draw.circle(self.screen, self.WHITE,
                                       (int((col_num + 1) * 100 + 50), int(row_num * 100 + 50) + self.BOARD_START_Y),
                                       self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)
                    pygame.draw.circle(self.screen, self.BLACK,
                                       (int((col_num + 1) * 100 + 50), int(row_num * 100 + 50) + self.BOARD_START_Y),
                                       self.CIRCLE_RADIUS, self.BORDER_WIDTH)
                elif marble == 'B':
                    pygame.draw.circle(self.screen, self.BLACK,
                                       (int((col_num + 1) * 100 + 50), int(row_num * 100 + 50) + self.BOARD_START_Y),
                                       self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)
                    pygame.draw.circle(self.screen, self.BLACK,
                                       (int((col_num + 1) * 100 + 50), int(row_num * 100 + 50) + self.BOARD_START_Y),
                                       self.CIRCLE_RADIUS, self.BORDER_WIDTH)
                elif marble == 'R':
                    pygame.draw.circle(self.screen, self.RED,
                                       (int((col_num + 1) * 100 + 50), int(row_num * 100 + 50) + self.BOARD_START_Y),
                                       self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)
                    pygame.draw.circle(self.screen, self.BLACK,
                                       (int((col_num + 1) * 100 + 50), int(row_num * 100 + 50) + self.BOARD_START_Y),
                                       self.CIRCLE_RADIUS, self.BORDER_WIDTH)

        # Show instructions
        notes = [
            "Welcome to Albert's Kuba Game!",
            "For a complete set of rules, please visit - https://sites.google.com/site/boardandpieces/list-of-games/kuba",
            "This window is merely a display capturing board state post-turns as well as current scores.",
            "Please perform all game actions and view all game-related error/information messages through the console."
        ]
        intro_message = instruction_font.render("Notes", False, (0, 0, 0))
        self.screen.blit(intro_message, (self.BOARD_START_X, self.BOARD_SIDE_LENGTH + self.BOARD_START_Y + 70))
        increment = 0
        for note in notes:
            note_text = message_font.render(note, False, (0, 0, 0))
            self.screen.blit(note_text, (self.BOARD_START_X, self.BOARD_SIDE_LENGTH + self.BOARD_START_Y + 100 + increment))
            increment += 20

        # Show scores
        player1_red_count = message_font.render(
            player_1.get_playername() + " currently has " + str(player_1.get_red_count()) + " red marbles.", False, (0, 0, 0))
        player2_red_count = message_font.render(
            player_2.get_playername() + " currently has " + str(player_2.get_red_count()) + " red marbles.", False, (0, 0, 0))
        self.screen.blit(player1_red_count, (self.BOARD_START_X, self.BOARD_SIDE_LENGTH + self.BOARD_START_Y + 10))
        self.screen.blit(player2_red_count, (self.BOARD_START_X, self.BOARD_SIDE_LENGTH + self.BOARD_START_Y + 30))

    def update_interface(self, ):
        """
        uses get_board method from KubaGame to braw game interface on pygame screen
        """
        pass




class KubaGame:
    """
    Represents a Kuba game with rules given in the ReadMe.
    It will need to communicate with the Player class to create and alter instances of that class.
    It will need to take care of all the functions that make playing the game possible (keeping track of whose turn it is,
    making moves and making sure that moves are valid, displaying and making changes to the board, keeping track of the
    winner, keeping track of the marbles currently on the board, keeping track of how many red marbles each player has.
    """

    def __init__(self, player1, player2):
        """
        initializes Kubagame instance.
        player_1 and player_2 are the two players of the game and they will be used to initialize Player class instances
        no return value
        """
        self._board = [['W', 'W', 'X', 'X', 'X', 'B', 'B'],
                       ['W', 'W', 'X', 'R', 'X', 'B', 'B'],
                       ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
                       ['X', 'R', 'R', 'R', 'R', 'R', 'X'],
                       ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
                       ['B', 'B', 'X', 'R', 'X', 'W', 'W'],
                       ['B', 'B', 'X', 'X', 'X', 'W', 'W']]
        self._players = [Player(player1[0], player1[1]), Player(player2[0], player2[1])]
        self._current_turn = None
        self._winner = None

        # for Ko rule checking
        self._last_slot_moved = None
        self._prev_direction = None

    def get_board(self):
        """
        returns board as a list of lists
        """
        return self._board

    def get_current_turn(self):
        """
        gets player name of whoever has the current turn.
        no parameters
        returns None if no one has made first move yet, otherwise returns name of player who has the current turn
        """
        return self._current_turn

    def get_player_from_name(self, playername):
        """
        returns Player instance given playername parameter
        :param playername: name of player you want to return instance of
        :return: Player instance with name "playername"
        """
        for player in self._players:
            if player.get_playername() == playername:
                return player

    def make_move(self, playername, coordinates, direction):
        """
        makes a move in the direction specified by the parameter on the marble at the coordinates parameter on behalf
        of the playername
        :param playername: name of player making move
        :param coordinates: coordinates of marble which the player wishes to make a move on
        :param direction: direction player wishes to move the marble
        :return: False if move is invalid (game has been won, not the player's turn, invalid coordinates, inaccessible marble)
        True if move is valid and was made
        """
        curr_player = self.get_player_from_name(playername)
        curr_player_marble = curr_player.get_marble_color()

        # if Game has already been won - return False
        if self._winner is not None:
            print("Game has already been won.")
            return False

        # if marble at coordinates isn't player's marble color, return false
        if self._board[coordinates[0]][coordinates[1]] != curr_player_marble:
            print("That marble doesn't belong to you!")
            return False

        # if you knock your own marble off the table, return false
        if self.check_knock_own_marble(curr_player_marble, direction, coordinates) is True:
            print("You knocked your own marble off the table. Invalid move.")
            return False

        # if Ko rule is not followed, return false
        if coordinates == self._last_slot_moved:
            if direction == 'L' and self._prev_direction == 'R':
                print("Ko rule not followed. Invalid move.")
                return False
            if direction == 'R' and self._prev_direction == 'L':
                print("Ko rule not followed. Invalid move.")
                return False
            if direction == 'F' and self._prev_direction == 'B':
                print("Ko rule not followed. Invalid move.")
                return False
            if direction == 'B' and self._prev_direction == 'F':
                print("Ko rule not followed. Invalid move.")
                return False

        # branch depending on direction
        if direction == 'L':
            # if not at right edge of board and slot to right isn't a blank, marble isn't accessible
            if coordinates[1] != 6 and self.get_marble((coordinates[0], coordinates[1] + 1)) != 'X':
                # print("The marble to the left of this one is not accessible")
                return False

            # if starting game, set current turn to current player, if current turn != current player,
            # it's not current player's turn
            if self._current_turn is None:
                self._current_turn = playername
            elif self._current_turn != playername:
                # print("It is not this player's turn.")
                return False

            # use in while loop
            prev_slot = coordinates
            curr_is_empty = False

            # logic - move towards marbles in direction you are pushing until you encounter a space or
            # until you get to the left edge of the board. For each slot, copy the marble that is currently
            # in the previous slot into the current slot.
            while not curr_is_empty and prev_slot[1] != 0:
                curr_slot = (prev_slot[0], prev_slot[1] - 1)
                curr_is_empty = self.get_marble(curr_slot) == 'X'
                if prev_slot == coordinates:
                    old_prev_marble = self.get_marble(prev_slot)
                else:
                    old_prev_marble = old_curr_marble
                old_curr_marble = self.get_marble(curr_slot)
                self.set_marble(curr_slot, old_prev_marble)

                if prev_slot == coordinates:
                    self.set_marble(prev_slot, 'X')

                prev_slot = curr_slot

            # if at edge of board and the marble that was there was red, it was pushed off
            if prev_slot[1] == 0 and old_curr_marble == 'R':
                curr_player.inc_red_count()
        elif direction == 'R':
            if coordinates[1] != 0 and self.get_marble((coordinates[0], coordinates[1] - 1)) != 'X':
                print("The marble to the right of this one is not accessible")
                return False

            if self._current_turn is None:
                self._current_turn = playername
            elif self._current_turn != playername:
                print("It is not this player's turn.")
                return False

            prev_slot = coordinates
            curr_is_empty = False

            while not curr_is_empty and prev_slot[1] != 6:
                curr_slot = (prev_slot[0], prev_slot[1] + 1)
                curr_is_empty = self.get_marble(curr_slot) == 'X'
                if prev_slot == coordinates:
                    old_prev_marble = self.get_marble(prev_slot)
                else:
                    old_prev_marble = old_curr_marble
                old_curr_marble = self.get_marble(curr_slot)
                self.set_marble(curr_slot, old_prev_marble)

                if prev_slot == coordinates:
                    self.set_marble(prev_slot, 'X')

                prev_slot = curr_slot

            if prev_slot[1] == 6 and old_curr_marble == 'R':
                curr_player.inc_red_count()
        elif direction == 'F':
            if coordinates[0] != 6 and self.get_marble((coordinates[0] + 1, coordinates[1])) != 'X':
                print("The marble below this one is not accessible")
                return False

            if self._current_turn is None:
                self._current_turn = playername
            elif self._current_turn != playername:
                print("It is not this player's turn.")
                return False

            prev_slot = coordinates
            curr_is_empty = False

            while not curr_is_empty and prev_slot[0] != 0:
                curr_slot = (prev_slot[0] - 1, prev_slot[1])
                curr_is_empty = self.get_marble(curr_slot) == 'X'
                if prev_slot == coordinates:
                    old_prev_marble = self.get_marble(prev_slot)
                else:
                    old_prev_marble = old_curr_marble
                old_curr_marble = self.get_marble(curr_slot)
                self.set_marble(curr_slot, old_prev_marble)

                if prev_slot == coordinates:
                    self.set_marble(prev_slot, 'X')

                prev_slot = curr_slot

            if prev_slot[0] == 0 and old_curr_marble == 'R':
                curr_player.inc_red_count()
        elif direction == 'B':
            if coordinates[0] != 0 and self.get_marble((coordinates[0] - 1, coordinates[1])) != 'X':
                print("The marble above this one is not accessible")
                return False

            if self._current_turn is None:
                self._current_turn = playername
            elif self._current_turn != playername:
                print("It is not this player's turn.")
                return False

            prev_slot = coordinates
            curr_is_empty = False

            while not curr_is_empty and prev_slot[0] != 6:
                curr_slot = (prev_slot[0] + 1, prev_slot[1])
                curr_is_empty = self.get_marble(curr_slot) == 'X'
                if prev_slot == coordinates:
                    old_prev_marble = self.get_marble(prev_slot)
                else:
                    old_prev_marble = old_curr_marble
                old_curr_marble = self.get_marble(curr_slot)
                self.set_marble(curr_slot, old_prev_marble)

                if prev_slot == coordinates:
                    self.set_marble(prev_slot, 'X')

                prev_slot = curr_slot

            if prev_slot[0] == 6 and old_curr_marble == 'R':
                curr_player.inc_red_count()

        self._last_slot_moved = prev_slot
        self._prev_direction = direction

        # check for winner via 7 red marbles
        for player in self._players:
            if player.get_red_count() == 7:
                self._winner = player.get_playername()

        # check for winner via knocking all of other player's marbles off
        if self.get_marble_count()[0] == 0:
            for player in self._players:
                if player.get_marble_color() == 'B':
                    self._winner = player.get_playername()
        elif self.get_marble_count()[1] == 0:
            for player in self._players:
                if player.get_marble_color() == 'W':
                    self._winner = player.get_playername()

        # at end of move, set current turn to be name of other player
        if curr_player == self._players[0]:
            self._current_turn = self._players[1].get_playername()
        else:
            self._current_turn = self._players[0].get_playername()

        return True

    def check_knock_own_marble(self, marble_color, direction, coordinates):
        """
        used within the make_move method to check if a potential move will knock own's own
        marble off the board
        :param marble_color: color of player's marble
        :param direction: direction of move, same as make_move parameter
        :param coordinates: coordinates of slot to move, same as make_move parameter
        :return: True if move will knock own marble off the board, False if it won't
        """
        curr_spot = coordinates

        if direction == 'L':
            while self.get_marble(curr_spot) != 'X' and curr_spot[1] != 0:
                curr_spot = (curr_spot[0], curr_spot[1] - 1)

            if curr_spot[1] == 0 and self.get_marble(curr_spot) == marble_color:
                return True
            else:
                return False

        if direction == 'R':
            while self.get_marble(curr_spot) != 'X' and curr_spot[1] != 6:
                curr_spot = (curr_spot[0], curr_spot[1] + 1)

            if curr_spot[1] == 6 and self.get_marble(curr_spot) == marble_color:
                return True
            else:
                return False

        if direction == 'F':
            while self.get_marble(curr_spot) != 'X' and curr_spot[0] != 0:
                curr_spot = (curr_spot[0] - 1, curr_spot[1])

            if curr_spot[1] == 0 and self.get_marble(curr_spot) == marble_color:
                return True
            else:
                return False

        if direction == 'B':
            while self.get_marble(curr_spot) != 'X' and curr_spot[0] != 6:
                curr_spot = (curr_spot[0] - 1, curr_spot[1])

            if curr_spot[1] == 0 and self.get_marble(curr_spot) == marble_color:
                return True
            else:
                return False

    def get_winner(self):
        """
        gets name of winner
        no parameters
        :return: name of winner, None if no player has won yet
        """
        return self._winner

    def get_captured(self, playername):
        """
        gets the player instance's red marble count data member
        :param playername: name of player you want red marble count of
        :return: player instances red marble count data member
        """

        return self.get_player_from_name(playername).get_red_count()

    def get_marble(self, coordinates):
        """
        returns what is present at the coordinates parameter on the board
        :param coordinates: coordinates of board spot for which you want to see what is present there
        :return: return X, W, B, R, depending on what is present at the coordinates location
        """
        return self._board[coordinates[0]][coordinates[1]]

    def set_marble(self, coordinates, marble_color):
        """
        set's board slot at coordinates position to be marble_Color parameter
        :param coordinates: coordinates of the slot on board you want to change color of
        :param marble_color: color you want to change that slot to
        :return: none
        """
        self._board[coordinates[0]][coordinates[1]] = marble_color

    def get_marble_count(self):
        """
        gets number of white, black, and red marbles as tuple in the order (W, B, R) by iterating through board
        and accumulating counts for each marble
        no parameters
        :return: tuple of counts of white, black, and red marbles currently on board
        """

        white_count = 0
        black_count = 0
        red_count = 0

        for sublist in self._board:
            for space in sublist:
                if space == 'W':
                    white_count += 1
                elif space == 'B':
                    black_count += 1
                elif space == 'R':
                    red_count += 1

        return white_count, black_count, red_count

    def display_board(self):
        """
        no parameters, displays game board to the console
        :return: none
        """
        for num in range(7):
            print(self._board[num])


class Player:
    """
    represents a player of the Kuba game. will be used by KubaGame class to track Player data
    It will track player name, color of ball, and how many red balls it has captured.
    """

    def __init__(self, name, marble_color):
        """
        uses KubaGame initial parameters to initialize Player instance. Also has red_marble_count data member, initialized
        to 0.
        :param name: name of player
        :param marble_color: player's marble color
        no return value
        """
        self._name = name
        self._marble_color = marble_color
        self._red_marble_count = 0

    def get_playername(self):
        """
        no parameters
        returns playername of instance
        :return: playername data member
        """
        return self._name

    def get_marble_color(self):
        """
        no parameters
        returns marble_color of instance
        :return: marble_color data member
        """
        return self._marble_color

    def get_red_count(self):
        """
        no parameters
        returns red_marble_count of instance
        :return: red_marble_Count data member
        """
        return self._red_marble_count

    def inc_red_count(self):
        """
        no parameters
        increments red_marble_count data member
        :return: no return value
        """
        self._red_marble_count += 1


if __name__ == "__main__":

    player_1 = input("Please enter the name and marble color of the first player as a tuple. (Ex. ('PlayerA', 'W')): ")
    player_1_as_tuple = tuple(player_1.split(','))
    player_2 = input("Please enter the name and marble color of the second player as a tuple. (Ex. ('PlayerB', 'B')): ")
    player_2_as_tuple = tuple(player_2.split(','))
    my_game = KubaGame(player_1_as_tuple, player_2_as_tuple)

    while my_game.get_winner() is None:
        my_pygame = PyGameFeatures(my_game.get_board(), my_game.get_player_from_name(player_1_as_tuple[0]),
                                   my_game.get_player_from_name(player_2_as_tuple[0]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()

        if my_game.get_current_turn() is None:
            coordinates = input(
                player_1_as_tuple[0] + ", please provide the coordinates (as a tuple in the format (row, column) of the marble you would like to move: ")
            coords_as_tuple = tuple(map(int, coordinates.split(',')))
            direction = input(player_1_as_tuple[0] + ", please provide the direction (L, R, F, or B) you would like to move to marble towards: ")
            my_game.make_move(player_1_as_tuple[0], coords_as_tuple, direction)
        else:
            coordinates = input(
                my_game.get_current_turn() + ", please provide the coordinates (as a tuple in the format (row, column) of the marble you would like to move: ")
            coords_as_tuple = tuple(map(int, coordinates.split(',')))
            direction = input(
                my_game.get_current_turn() + ", please provide the direction (L, R, F, or B) you would like to move to marble towards: ")
            my_game.make_move(my_game.get_current_turn(), coords_as_tuple, direction)




