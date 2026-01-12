from enum import Enum
from typing import List
from functools import total_ordering
import random

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Value(Enum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K" 
 

class Card:
    def __init__(self, suit: Suit, value: Value):
        self.suit = suit
        self.value = value
        self.bj_value = self.compute_bj_value()
    
    def __str__(self):
        return ("┌─────┐\n"
                f"│{self.value.value}    │\n"
                f"│  {self.suit.value}  │\n"
                f"│    {self.value.value}│\n"
                "└─────┘")
    
    def compute_bj_value(self):
        if self.value == Value.ACE:
            return 11
        elif self.value in (Value.JACK, Value.QUEEN, Value.KING):
            return 10
        else:
            return int(self.value.value)
    
    def ascii_lines(self) -> list[str]:
        if self.value == Value.TEN:
            return ["┌─────┐",
                f"│{self.value.value}   │",
                f"│  {self.suit.value}  │",
                f"│   {self.value.value}│",
                "└─────┘"]
        return ["┌─────┐",
                f"│{self.value.value}    │",
                f"│  {self.suit.value}  │",
                f"│    {self.value.value}│",
                "└─────┘"]


class Deck:
    def __init__(self):
        self.deck = [Card(suit,value) for suit in Suit for value in Value]

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()

    def reset(self):
        self.deck = [Card(suit,value) for suit in Suit for value in Value]

@total_ordering
class Hand:
    def __init__(self):
        self.hand: List[Card] = []

    def add_card(self, card: Card):
        self.hand.append(card)
    
    def flush(self):
        self.hand.clear()
    
    def value(self):
        total = sum(card.bj_value for card in self.hand)
        ace_count = sum(card.value == Value.ACE for card in self.hand)

        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        return total
    
    def useful_ace(self):
        total = sum(card.bj_value for card in self.hand)
        ace_count = sum(card.value == Value.ACE for card in self.hand)

        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        return ace_count > 0

    
    def bust(self):
        return self.value() > 21
    
    def blackjack(self):
        return self.value() == 21 and len(self.hand) == 2

    def __eq__(self, other):
        if not isinstance(other, Hand):
            return NotImplemented
        
        return self.value() == other.value()
    
    def __lt__(self, other):
        if not isinstance(other, Hand):
            return NotImplemented
        
        return self.value() < other.value()
    
    def __str__(self):
        if not self.hand:
            return "<empty hand>"
        
        ascii_cards = [card.ascii_lines() for card in self.hand]
        height = len(ascii_cards[0])

        return "\n".join(
            " ".join(card[i] for card in ascii_cards) for i in range(height)
        ) 


