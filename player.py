DEBUG = True

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] | None = None
        self.pickup_pile: list[Card] | None = None
        self.points = 0
        self.lifetime_points = 0
        self.lifetime_placements: list[int] = []

    def pickup_pile_sum(self):
        return sum([card.cattle_heads for card in self.pickup_pile])

    def print_hand(self):
        if DEBUG:
            print(f'{self.name} hand {self.hand}')

    '''
    Play smallest difference card that isn't on a 5 pile
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
