from collections import Counter
from typing import NamedTuple

x = open('day7.txt').read()
# 250970819
# 251942097
card_trans = {
    'A': 14, 'K': 13, 'Q': 12, 'T': 10, 'J': 1
}

class HandType:
    FiveKind = 7
    FourKind = 6
    FullHouse = 5
    ThreeKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1


class Hand(NamedTuple):
    hand_type: int
    hand: tuple[int, int, int, int, int]

    def __repr__(self):
        match self.hand_type:
            case 1:
                n = 'High Card'
            case 2:
                n = 'One Pair'
            case 3:
                n = 'Two Pair'
            case 4:
                n = 'Three of a Kind'
            case 5:
                n = 'Full House'
            case 6:
                n = 'Four of a Kind'
            case 7:
                n = 'Five of a Kind'
        return f'[{n} {self.hand}]'


def get_hand(h_string: str) -> Hand:
    hand = []
    for c in h_string:
        hand.append(int(card_trans.get(c, c)))
    mc = 1
    for c, _ in Counter(hand).most_common():
        if c != 1:
            mc = c
            break
    newhand = hand[:]
    for i, c in enumerate(newhand):
        if c == 1:
            newhand[i] = mc
    hc = Counter(newhand)
    if len(hc) == 5:
        ctype = HandType.HighCard
    if len(hc) == 4:
        ctype = HandType.OnePair
    if len(hc) == 3:
        if max(hc.values()) == 2:
            ctype = HandType.TwoPair
        else:
            ctype = HandType.ThreeKind
    if len(hc) == 2:
        if max(hc.values()) == 4:
            ctype = HandType.FourKind
        else:
            ctype = HandType.FullHouse
    if len(hc) == 1:
        ctype = HandType.FiveKind
    return Hand(ctype, tuple(hand))


hands = []
for line in x.split('\n'):
    if not line:
        continue
    hand_str, bid = line.split(' ')
    bid = int(bid)
    hands.append((get_hand(hand_str), int(bid)))

total = 0
for rank, (hand, bid) in enumerate(sorted(hands), 1):
    print(bid, rank, hand)
    total += bid * rank
print(total)
