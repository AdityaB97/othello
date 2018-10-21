import string

class Board:
    ###############################################################################
    # Initialization and getter/setter methods
    ###############################################################################


    def __init__(self, length=8):
        self.length = length
        self.row_names = [str(i) for i in range(1, self.length + 1)]
        self.column_names = list(string.ascii_lowercase[:self.length])
        self.initialize()
        

    def initialize(self):
        '''Initializes the board as specified in the spec'''
        self.board = [[None for j in range(self.length)] for i in range(self.length)]
        midpoint = self.length // 2
        self.set_piece(midpoint - 1, midpoint - 1, 1)
        self.set_piece(midpoint - 1, midpoint, 0)
        self.set_piece(midpoint, midpoint - 1, 0)
        self.set_piece(midpoint, midpoint, 1)
    
    
    def get_piece(self, i, j):
        return self.board[i][j]
    
    
    def set_piece(self, i, j, value):
        self.board[i][j] = value


    ###############################################################################
    # These methods are for validating the user input, and converting the
    # action format from a string to a pair fo indices
    ###############################################################################
        
    
    def assert_is_position_valid(self, position_as_string):
        '''Asserts that the given input action/position is in the right format'''
        assert type(position_as_string) == str, 'Input must be a string'
        assert len(position_as_string) == 2, 'The action must have exactly 2 characters'
        column, row = position_as_string
        assert column in self.column_names and row in self.row_names, 'The position you provided is outside the range of the board'

    
    def convert_position_to_indices(self, position_as_string):
        '''
        Takes in an action string like 'd3' and converts it to indices like (2,3)
        '''
        self.assert_is_position_valid(position_as_string)
        column, row = position_as_string
        return self.row_names.index(row), self.column_names.index(column)
    

    ###############################################################################
    # These methods deal with checking whether any actions exist, performing
    # an action, and verifying whether the input action is valid
    ###############################################################################


    def is_within_range(self, i, j):
        '''Returns true iff (i, j) is within the bounds of the board'''
        return (0 <= i < self.length) and (0 <= j < self.length)
    

    def generate_sequences(self, row, column):
        '''
        Generates all 'sequences' originating from the given row and column position I am
        using the term "sequence" to refer to what the spec calls a "row". That is, a line
        (or rather, a ray) of positions starting from one position and going in one direction
        along a row, column, or diagonal
        '''
        sequences = []
        for row_increment in (-1, 0, 1):
            for column_increment in (-1, 0, 1):
                if not (row_increment == 0 and column_increment == 0):
                    i, j = row, column
                    sequence = []
                    while self.is_within_range(i, j):
                        sequence.append((i, j))
                        i += row_increment
                        j += column_increment
                    sequences.append(sequence)
        assert len(sequences) == 8
        return sequences
    

    def is_sequence_outflanking(self, sequence, player):
        '''
        Returns true iff the given sequence outflanks the opponent of the given player.
        i.e. There must be an unbroken run of `(1 - player)` in the sequence, followed
        by `player` at the end of that run
        '''
        if len(sequence) < 3 \
            or self.get_piece(*sequence[1]) != 1 - player:
                return False
        for position in sequence[2:]:
            if self.get_piece(*position) == None:
                return False
            elif self.get_piece(*position) == 1 - player:
                continue
            elif self.get_piece(*position) == player:
                return True
    

    def is_position_taken(self, row, column):
        '''Returns true iff the given position is not open (i.e. it is taken)'''
        return self.get_piece(row, column) != None


    def is_action_valid(self, row, column, player):
        '''
        Returns true iff the given action is valid for the given player, i.e. that position
        is open, there is at least one sequence from that action position which outflanks
        the opponent
        '''
        sequences = self.generate_sequences(row, column)
        return (not self.is_position_taken(row, column)) and any([self.is_sequence_outflanking(sequence, player) for sequence in sequences])
    

    def has_available_action(self, player):
        '''Returns true iff the given player has an available action'''
        for row in range(self.length):
            for column in range(self.length):
                if self.is_action_valid(row, column, player):
                    return True
        return False
    

    def flip_sequence(self, sequence, player):
        '''
        Takes in a sequence of positions and a player (0 or 1).
        Flips all of the opponent's pieces between the first and second occurrences of this player in the sequence
        Assumes that the input sequence is valid (i.e. the player outflanks the opponent at this sequence)
        '''
        self.set_piece(*sequence[0], player)
        for position in sequence[1:]:
            if self.get_piece(*position) == player:
                break
            elif self.get_piece(*position) == 1 - player:
                self.set_piece(*position, player)
                

    ###############################################################################
    # These methods are for checking whether the game is over, and
    # determining the winning player
    ###############################################################################


    def flatten(self):
        '''Returns a flattened version of the board'''
        return [self.get_piece(i, j) for i in range(self.length) for j in range(self.length)]
    

    def is_full(self):
        '''Returns true iff the board has no open squares'''
        flattened_board = self.flatten()
        return not (None in flattened_board)
    

    def winning_player(self):
        '''
        Returns the winning player, i.e. the player with more disks. If they both
        have the same number of disks, it returns None
        '''
        flattened_board = self.flatten()
        number_of_ones, number_of_zeros = 0, 0
        
        for piece in flattened_board:
            if piece == 1:
                number_of_ones += 1
            else:
                number_of_zeros += 1
        
        margin = number_of_ones - number_of_zeros
        if margin > 0:
            return 1
        elif margin < 0:
            return 0
        else:
            return None


    ###############################################################################
    # This method prints the board
    ###############################################################################
        
    def print(self):
        '''Prints the board with nice-looking formatting (evenly spaced columns, etc.)'''
        # TODO: Clean this up more
        output_data =  [[''] + self.column_names] \
                + [[str(row_index + 1)] \
                + [str(e) if e is not None else '-' for e in self.board[row_index]] for row_index in range(len(self.board))]
        biggest_column_sizes = [max(map(len, col)) for col in zip(*output_data)]
        output_format = '\t'.join('{{:{}}}'.format(x) for x in biggest_column_sizes)
        output_table = [output_format.format(*row) for row in output_data]
        print('\n')
        print('\n'.join(output_table))
