from cards import Deck, Hand

class BlackJack:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.done = 0
    
    def hit(self):
        self.player_hand.add_card(self.deck.draw())
    
    def stay(self):
        pass

    def reset(self):
        self.player_hand.flush()
        self.dealer_hand.flush()
        self.deck.reset()
        self.deck.shuffle()

        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())

        reward = 0

        if self.player_hand.value() == 21 and self.dealer_hand.value() == 21:
            self.done = 1

        elif self.player_hand.value() == 21:
            self.done = 1            
            reward = 1

        elif self.dealer_hand.value() == 21:
            self.done = 1
            reward = -1

        return self.state(), reward, self.done

    def state(self):
        return (self.player_hand.value(), self.dealer_hand.hand[0].bj_value, self.player_hand.useful_ace())
    
    def step(self, action): # return state, reward, done
        if action == "hit":
            self.player_hand.add_card(self.deck.draw())
            if self.player_hand.bust():
                return self.state(), -1, 1
            
            return self.state(), 0, 0 #dummy

        elif action == "stay":
            while self.dealer_hand.value() < 17:
                self.dealer_hand.add_card(self.deck.draw())

            if self.dealer_hand.bust():
                return self.state(), 1, 1

            player_total = self.player_hand.value()
            dealer_total = self.dealer_hand.value()

            if player_total > dealer_total:
                return self.state(), 1, 1
            elif dealer_total > player_total:
                return self.state(), -1, 1
            else:
                return self.state(), 0, 1

    # def get_player_action(self) -> str:
    #     while True:
    #         action = input("Hit or stay? ").lower()
    #         action = action.strip()
    #         if action in ("hit", "stay"):
    #             return action
    #         print("Invalid input. Please type 'hit' or 'stay'.")
    
    # def run_match(self):
    #     self.player_hand.flush()
    #     self.dealer_hand.flush()
    #     self.deck.reset()
    #     self.deck.shuffle()

    #     self.player_hand.add_card(self.deck.draw())
    #     self.dealer_hand.add_card(self.deck.draw())
    #     self.player_hand.add_card(self.deck.draw())
    #     self.dealer_hand.add_card(self.deck.draw())

    #     if self.player_hand.value() == 21 and self.dealer_hand.value() == 21:
    #         return "Tie - Both Blackjack"

    #     if self.player_hand.value() == 21:
    #         self.done = 1            
    #         return "Player Blackjack"

    #     if self.dealer_hand.value() == 21:
    #         self.done = 1
    #         return "Dealer Blackjack"
        
    #     while True:
    #         print("="*40)
    #         print("Current Hands ")
    #         print("="*40)
    #         print("Player : ")
    #         print(self.player_hand)
    #         print("Dealer : ")
    #         print(self.dealer_hand.hand[0])
    #         print("="*40)
    #         action = self.get_player_action()

    #         if action == "hit":
    #             self.player_hand.add_card(self.deck.draw())
    #             if self.player_hand.bust():
    #                 self.done = 1
    #                 return "Player Bust - Dealer Wins"

    #         elif action == "stay":
    #             break

    #     while self.dealer_hand.value() < 17:
    #         self.dealer_hand.add_card(self.deck.draw())

    #     if self.dealer_hand.bust():
    #         self.done = 1 
    #         return "Dealer Bust - Player Wins"

    #     player_total = self.player_hand.value()
    #     dealer_total = self.dealer_hand.value()

    #     if player_total > dealer_total:
    #         self.done = 1            
    #         return "Player Wins"
    #     elif dealer_total > player_total:
    #         self.done = 1
    #         return "Dealer Wins"
    #     else:
    #         return "Tie"

    
    
      