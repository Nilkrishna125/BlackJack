# print(" ____ ")
# print("|A   |")
# print("| \u2660  |")
# print("|___A|")


# print("┌─────┐\n│A    │")
# print("│  ♠  │")
# print("│    A│\n└─────┘")


# from cards import Deck
# from blackjack import BlackJack

# deck = Deck()
# deck.shuffle()

# game = BlackJack()
# output = game.run_match()
# print(game.player_hand)
# print(game.dealer_hand)
# print(output)

# a = 1_000
# b = 1_007
# print(a*b)

# import numpy as np
# l = np.array([0,3,5,6])
# a = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
# a[l] = 1
# print(a)

# import numpy as np
# print(np.arange(5))

import numpy as np
def f(a:tuple):
    return a[0]

grid = np.empty((10,10), dtype=tuple)
for i in range(10):
    for j in range(10):
        grid[i][j] = (i,j)
        
grid = f(grid)
print(grid)