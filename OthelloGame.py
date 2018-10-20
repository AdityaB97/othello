from Board import Board

class OthelloGame:
    def __init__(self):
        self.current_player = 0
        self.board = Board()
        self.update_action_availability()
        
    ###############################################################################
    # These update methods are called every turn. They update the 
    # self.is_action_available and self.current_player variables
    ###############################################################################

    def update_action_availability(self):
        self.is_action_available = [self.board.has_available_action(player) for player in (0, 1)]

    def update_current_player(self):
        self.current_player = 1 - self.current_player


    ###############################################################################
    # The methods implementing action validation and taking an action
    ###############################################################################


    def assert_that_action_is_valid(self, row, column):
        assert not self.board.is_position_taken(row, column), 'That position is already taken'
        assert self.board.is_action_valid(row, column, self.current_player), 'The action you provided does not outflank the opponent'
        
        
    def take_action(self, row, column):
        sequences = self.board.generate_sequences(row, column)
        for sequence in sequences:
            if self.board.is_sequence_outflanking(sequence, self.current_player):
                self.board.flip_sequence(sequence, self.current_player)
    
    
    def play_turn(self):
        if not self.is_action_available[self.current_player]:
            print(f'Player {self.current_player} has no actions available. Moving to player {1 - self.current_player}')
        else:
            input_action = input()
            action = self.board.convert_position_to_indices(input_action)
            row, column = action
            self.assert_that_action_is_valid(row, column)
            self.take_action(row, column)
        
        self.update_action_availability()
        self.update_current_player()
    
    
    ###############################################################################
    # The methods controlling the overall flow of the game
    ###############################################################################

    
    def is_game_over(self):
        # Note: self.is_action_available is a tuple with a boolean for each player
        return self.board.is_full() or (not any(self.is_action_available))
    

    def end(self):
        winner = self.board.winning_player()
        if winner == None:
            print('The game has ended in a tie')
        else:
            print(f'The game has ended. The winner is player {winner}')
    
    
    def run(self):
        while True:
            try:
                if self.is_game_over():
                    self.end()
                    return
                else:
                    print('\nHere is the current board:')
                    self.board.print()
                    print(f"\nPlease input player {self.current_player}'s next action")
                    while True:
                        try:
                            self.play_turn()
                            break
                        except AssertionError as e:
                            print(e)
            except KeyboardInterrupt:
                print('\nYou have terminated the game\n')
                break
            

            
        
        
