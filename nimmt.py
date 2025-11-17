import random

class Card:
    @staticmethod
    def calculate_cattle_heads(num):
        match num:
            case 55:
                return 7
            case num%11==0:
                return 5
            case num%10==0:
                return 3
            case num%5==0:
                return 2
            case _:
                return 1

    def __init__(self, num):
        self.num = num
        self.cattle_heads = self.calculate_cattle_heads(num)


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] | None = None
        self.pickup: list[Card] | None = None
        self.points = 0

    '''
    Current logic is just to play a random card.
    Will separate this into separate strategy classes that inherit from the main Player class later.
    '''
    def play(self, play_piles: list[MiddlePile]): 
        random.shuffle(self.hand)
        return self.hand.pop()

    '''
    Current logic is to pick up pile with lowest sum of cattle heads
    '''
    def pickup_choice(self, play_piles: list[MiddlePile]) -> int: # index of pickup
        cattle_head_sums = [pile.cattle_head_sum() for pile in play_piles]
        index = 0
        cattle_head_min = cattle_head_sums[0]
        for i in range(len(cattle_head_sums)):
            if cattle_head_sums[i]<cattle_head_min:
                cattle_head_min = cattle_head_sums[i]
                index = i
        return index


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
    def __init__(self):
        self.cards : list[Card] | None = None

    def play_card(self, card):
        if self.cards = 5: # middle pile is full
            ret_cards = self.cards
            self.cards = [card]
            return self.cards
        self.cards.append(card)

    def cattle_head_sum(self):
        return sum([card.cattle_heads for card in self.cards])


class Round:
    def __init__(self, players: list[Player], deck: Deck):
        for player in players:
            player.hand = deck.deal(10)
        self.play_piles = [MiddlePile() for i in range(4)]

    def play_card(self, card: Card, player: Player):
        if card.num < min([pile[-1].num for pile in self.play_piles]): # smaller than end of all piles
            self.play_piles[player.pickup_choice(self.play_piles)].play_card(card) # play on chosen pile
        else: # viable pile to play on
            candidate_val = 105
            for i in range(len(self.play_piles)):
                if self.play_piles[i]
            lowest_playable_pile = 
            self.play_piles[]


    def play_round(self):
        played_cards: tuple[Card, Player] = [player.play(self.play_piles), player for player in self.players]
        played_cards = sorted(played_cards, key=lambda x: x[0].num)
        
