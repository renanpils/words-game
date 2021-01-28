from words_manager import *


# Imports:
import random
import numpy as np
import time 

# Game constants:
CARDS_ON_GAME = 25
CARDS_PER_TEAM = 10
DEATH_CARDS = 2
TEAMS = 2

generator = WordSpitter('resources/br-utf8.txt')


# Definitions:
class Player():
    def __init__(self, name, ip, host= False):
        self.name = name
        self.ip_address = ''
        self.score = 0
        self.identifier = 0
        self.host = False
        self.team = 0

    
    def increase_score(self):
        self.score += 1

    def print_player_info(self):
        print(self.name, self.team, self.identifier)

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address

    def set_team(self, team):
        self.team = team

    def add_score(self, points):
        self.score += points

    def get_team(self):
        return self.team

class Card():
    def __init__(self, word):
        self.word = word
        self.picked = False
        self.picked_by_team = 0
        self.owner_team = None #1, 2 or 9 (Death Card)

    def pick_card(self, who: Player):
        ''' Player will pick a card '''
        self.picked = True
        self.picked_by_team = who.get_team()
    
    def card_info_str(self):
        s = 10
        s_fmt = '{: <' + str(s) +'}'
        string_formated = str(s_fmt.format(self.word) if len(self.word)<s else self.word[0:s]) + ' ' + \
              ('Not Picked', 'Picked    ')[self.picked] + \
              ' by '+ str(self.picked_by_team) + \
              ' own: ' + str(self.owner_team)
        return string_formated

class Game:
    def __init__(self):
        # Generate new list of words
        self.words = generator.sort_words(CARDS_ON_GAME)
        self.cards = [Card(word) for word in self.words]
        self.players = {}
        self.card_count = {None: 0, 1: 0, 2: 0, 9: 0}
        self.game_over = False
        self.pick_history = [] #list of dictionaries.
        self.team = {1: [], 2: []}
        self.turn = {'team': np.random.randint(2)+1, 'player': ''}
    
    def print_cards(self):
        for i, card in enumerate(self.cards):
            print('{:2.0f}'.format(i), card.card_info_str())


    def pick_a_card(self, who_str:str, card_idx:int):

        if not self.cards[card_idx].picked:
        
            self.cards[card_idx].pick_card(self.players[who_str])
            print('Card {} picked: {} by {}'.format(card_idx ,self.cards[card_idx].word, self.players[who_str].name))
            
            # self.cards[card_idx].word
            # self.players[who_str].name

            # Check:
            if self.cards[card_idx].owner_team == self.players[who_str].team:
                print('   chicken dinner!')

            elif self.cards[card_idx].owner_team == 9:
                print('   ops you lose!')

            else:
                print('   points to the other team!')

            # Refresh the card count
            self.card_count[self.cards[card_idx].owner_team] += 1

            # append a dictionary to pick_history:
            self.pick_history.append( {'timestamp'   :time.time(), 
                                       'player name' :who_str, 
                                       'card index'  :card_idx, 
                                       'card word'   :self.cards[card_idx].word,
                                       'correct team':self.cards[card_idx].owner_team == self.players[who_str].team,
                                       'death card'  :self.cards[card_idx].owner_team == 9,
                                       'event'       :'card picked' })
            return 1

        else:
            print('card already picked')

            return 0
    
    # Def game management functions ========================================
    def print_history(self):
        for i in self.pick_history:
            print(i)

    def start_game(self):
        # what do i need to make sure to start the game?
            # Check whether teams are correct
            # Check if any card has been picked
            # Make sure game is not over
        
        # set turns
        pass 


    def check_game(self):
        if self.card_count[1] == CARDS_PER_TEAM:
            # print('game over! team 1 wins!')
            # print('winner word: ', self.pic)
            self.game_over = True
            return 1, self.game_over
        
        elif self.card_count[2] == CARDS_PER_TEAM:
            # print('game over! team 2 wins!')
            self.game_over = True
            return 2, self.game_over

        elif self.card_count[9] >= 1:
            # print('game over')
            self.game_over = True
            return 9, self.game_over
        
        else:
            return 0, self.game_over
    
    def next_turn(self):
        # compute next turn.
        pass

    def sort_cards_for_teams(self, teams_cards_n:int = CARDS_PER_TEAM, death_cards_n:int = DEATH_CARDS ):
        # Create a list:
        idxs = np.random.permutation(len(self.cards))
        team1_idx = idxs[0:teams_cards_n]
        team2_idx = idxs[teams_cards_n:2*teams_cards_n]
        death_card_idx = idxs[(2*teams_cards_n):(2*teams_cards_n+death_cards_n)]
        
        for i in team1_idx:
            self.cards[i].owner_team = 1
        
        for i in team2_idx:
            self.cards[i].owner_team = 2
        
        for i in death_card_idx:
            self.cards[i].owner_team = 9



    # Def player management functions
    def add_player(self, name_str:str, player_obj: Player):
        
        if name_str in self.players:
            name_str = name_str + '207'
                    
        self.players[name_str] = player_obj
        # print('Adding {} on ip {} '.format(name_str, player_obj.ip_address) )
    
    def remove_player(self, name_str:str):
        if name_str in self.players:
            del self.players[name_str]

    def set_player_ip(self, name_str: str, ip_address:str):
        try:
            self.players[name_str].ip_address = ip_address
        except:
            print('ip_adress not set: ', ip_address, ' invalid player name_str: ', name_str) 

    def set_player_team(self, name_str:str, team: int):
        if name_str in self.players:
            self.players[name_str].set_team(team)
        else:
            print('ops, no player with this name. Add player before') 

    def get_all_players(self):
        return self.players

    def get_player(self, name:str):
        if name in self.players:
            return self.players[name]
        else:
            return None
    
    def print_players(self):
        for p in self.players:
            # as self.players is dict, it will return a key
            print(p, self.players[p].ip_address, ' team: ',self.players[p].team)

if __name__ == '__main__':
    print('Start Execution: ')
    # Create a New game
    game = Game()
    # game.print_cards()
    
    # Test Variables:
    player_names_list = ['John', 'Flea', 'Anthony', 'Chad', 'Josh', 'Dave']
    player_teams = [1, 2, 1, 1, 2, 2,]
    ip_list = ['10.0.0.106', '10.0.0.106', '10.0.0.106', '10.0.0.106','10.0.0.106','10.0.0.106']
    
    # Create random pick sequences
    pick_list = list(np.random.permutation(CARDS_ON_GAME)[0:10])
    player_pick_list = list([np.random.randint(len(player_names_list)) for i in range(10)])


    # Create players: add or remove
    for name, ip, tm in zip(player_names_list, ip_list, player_teams):
        game.add_player(name, Player(name, ip))
        game.set_player_ip(name, ip)
        game.set_player_team(name, tm)

    #Sort teams randomly
    
    game.add_player('Renan', Player('Renan', '0.0.0.0', host= True))
    game.remove_player('Renan')

    
    # print(pick_list)
    # print(player_pick_list)

    # Sort the words for each team:
    game.sort_cards_for_teams()

    # Print players list to console
    print('Players at the start of the game: ')
    game.print_players()
    
    # Here is how the game will run, picking cards and checking the game
    for pick, pick_player_idx in zip(pick_list, player_pick_list):
        game.pick_a_card(player_names_list[pick_player_idx], pick)
        
        check, game_over = game.check_game()
        if game_over:
            if check == 1:
                print('team 1 wins')
            elif check == 2:
                print('team 2 wins')
            elif check == 9:
                print('GAME OVER')
        else:
            pass
        # input(' ')

    print('-------------------')
    # game.print_cards()

    # game.print_history()

    print('End of program... ')
    # input('press Enter to finish.')

