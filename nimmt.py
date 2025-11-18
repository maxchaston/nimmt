#!/usr/bin/env python3
import random

class Card:
    @staticmethod
    def calculate_cattle_heads(num: int):
        if num == 55:
            return 7
        elif num%11==0:
            return 5
        elif num%10==0:
            return 3
        elif num%5==0:
            return 2
        else:
            return 1

    def __init__(self, num):
        self.num = num
        self.cattle_heads = self.calculate_cattle_heads(num)

    def __repr__(self):
        return f'{self.num}'


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] | None = None
        self.pickup_pile: list[Card] | None = None
        self.points = 0
        self.lifetime_points = 0
        self.lifetime_placements: list[int] = []

    '''
    Current logic is just to play a random card.
    Will separate this into separate strategy classes that inherit from the main Player class later.
    '''
    def play(self, play_piles: list['MiddlePile']): 
        random.shuffle(self.hand)
        return self.hand.pop()

    '''
    Current logic is to pick up pile with lowest sum of cattle heads
    '''
    def pickup_choice(self, play_piles: list['MiddlePile']) -> int: # index of pickup
        cattle_head_sums = [pile.cattle_head_sum() for pile in play_piles]
        index = 0
        cattle_head_min = cattle_head_sums[0]
        for i in range(len(cattle_head_sums)):
            if cattle_head_sums[i]<cattle_head_min:
                cattle_head_min = cattle_head_sums[i]
                index = i
        return index

class RandomPlayer(Player):
    '''
    Current logic is just to play a random card.
    Will separate this into separate strategy classes that inherit from the main Player class later.
    '''
    def play(self, play_piles: list['MiddlePile']): 
        random.shuffle(self.hand)
        return self.hand.pop()

    '''
    Current logic is to pick up a random pile
    '''
    def pickup_choice(self, play_piles: list['MiddlePile']) -> int: # index of pickup
        return random.randint(0,3)


class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.contents = [Card(i) for i in range(1,105)]

    def shuffle(self):
        random.shuffle(self.contents)

    def deal(self, num) -> list[Card]: 
        ret = []
        for i in range(num):
            ret.append(self.contents.pop())
        return ret


class MiddlePile:
    def __init__(self, card: Card):
        self.cards : list[Card] = card

    def play_card(self, card: Card):
        if len(self.cards) == 5 or card.num<self.cards[-1].num: # middle pile is full or smaller number
            ret_cards = self.cards
            self.cards = [card]
            return self.cards
        self.cards.append(card)
        return None

    def cattle_head_sum(self):
        return sum([card.cattle_heads for card in self.cards])

    def __getitem__(self, index):
        return self.cards[index]

    def __setitem__(self, index, value):
        self.cards[index] = value

    def __repr__(self):
        return str(self.cards)


class Round:
    def __init__(self, players: list[Player], deck: Deck):
        deck.reset()
        deck.shuffle()
        for player in players:
            player.hand = []
            player.pickup_pile = []
            player.hand = deck.deal(10)
            print(f'{player.name} hand {player.hand}')
        self.play_piles = [MiddlePile(deck.deal(1)) for i in range(4)]
        self.players = players

    def print_table(self):
        print('Current table')
        print(*self.play_piles, sep='\n')

    def play_card(self, card: Card, player: Player):
        print(f'{player.name} playing card {card}')
        if card.num < min([pile[-1].num for pile in self.play_piles]): # smaller than end of all piles
            cards_to_pickup = self.play_piles[player.pickup_choice(self.play_piles)].play_card(card) # play on chosen pile
        else: # viable pile to play on
            candidate_diff = 105
            candidate_index = -1
            for i in range(len(self.play_piles)):
                if self.play_piles[i][-1].num < card.num and abs(card.num-self.play_piles[i][-1].num) < candidate_diff:
                    candidate_diff = abs(card.num-self.play_piles[i][-1].num)
                    candidate_index = i
            lowest_playable_pile = self.play_piles[candidate_index]
            cards_to_pickup = lowest_playable_pile.play_card(card)
        if cards_to_pickup:
            player.pickup_pile = player.pickup_pile + cards_to_pickup

    def play_turn(self):
        played_cards: tuple[Card, Player] = [(player.play(self.play_piles), player) for player in self.players]
        played_cards = sorted(played_cards, key=lambda x: x[0].num)
        for (card, player) in played_cards:
            self.play_card(card, player)
        self.print_table()

    def play_round(self):
        self.print_table()
        for i in range(10):
            self.play_turn()
        for player in self.players:
            player.points += sum([card.cattle_heads for card in player.pickup_pile])
            # print([card.cattle_heads for card in player.pickup_pile])

class Game:
    def __init__(self, players: list[Player]):
        self.players = players
        for player in self.players:
            player.points = 0
        self.deck = Deck()

    def start(self):
        round_count = 1
        while max([player.points for player in self.players]) < 66:
            print(f'\n\nGAME: Starting round {round_count}')
            curr_round = Round(self.players, self.deck)
            curr_round.play_round()
            round_count += 1
        print([f'{player.name}: {player.points}' for player in self.players])
        for player in self.players:
            player.lifetime_points += player.points

        player_results = sorted(self.players, key=lambda x: x.points)
        # print([(p.name, p.points) for p in player_results])
        # print()
        for i in range(len(player_results)):
            player_results[i].lifetime_placements.append(i+1)            

def avg(x):
    return sum(x)/len(x)

def main():

    player_1 = Player("Player 1")
    player_2 = RandomPlayer("Random Player 2")
    player_3 = RandomPlayer("Random Player 3")
    player_4 = RandomPlayer("Random Player 4")

    players = [player_1, player_2, player_3, player_4]

    matches = 200000
    for i in range(matches):
        if i%1000 == 0:
            print(f'Starting game {i}')
        game = Game([player_1, player_2, player_3, player_4])
        game.start()
    print([f'{player.name}: {player.lifetime_points} (avg placement: {avg(player.lifetime_placements)}) (avg score: {player.lifetime_points/matches})' for player in players])

    # game = Game([player_1, player_2, player_3, player_4])
    # game.start()


if __name__ == "__main__":
    main()
