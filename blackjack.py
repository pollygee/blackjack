# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 950x392 - source: jfitz.com
CARD_SIZE = (73, 98)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize global variables
in_play = False
outcome = ""
score = 0
busted = False

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", self.suit, self.rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(self.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(self.suit)))
        #card_loc = (card_size[0] * (0.5 + RANKS.index(self.rank)), card_size[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE)
        #canvas.draw_image(card_images, card_loc, card_size, [pos[0] + card_size[0] / 2, pos[1] + card_size[1] / 2], card_size)

# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        self.value = 0
        return self.hand 
        
    def __str__(self):
        s1 = "Hand contains " 
        for c in self.hand:
            s1 += str(c) + " "
        return s1

    def add_card(self, card):
        self.hand.append(card)	

    # count aces as 1, if the hand has an ace, then add 10 to hand value if don't bust
    def get_value(self):
        self.value = 0
        ace = False
        for card in self.hand:
            self.value += VALUES[card.get_rank()]
            if (card.get_rank() == 'A'):
                ace = True
        if ace == True:    
            if (self.value + 10) < 21:
                self.value = self.value + 10
                
                    
        return self.value    
            
    def busted(self):
        if self.value > 21:
            return True
        return False
    
    def draw(self, canvas, p):
        count = 0
        for c in self.hand:
            if count < 5:
                c.draw(canvas, p)
                p[0] += 73
                count += 1
                  
# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        return self.deck
    
    def __str__(self):
        s1 = "Deck contains " 
        for c in self.deck:
            s1 += str(c) + " "
        return s1

    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck

    def deal_card(self):
        d = self.deck[-1]
        self.deck.remove(d)
        return d

#define callbacks for buttons
def deal():
    global outcome, in_play, dealer_hand, player_hand, directions, busted, score, outcome
    directions = 'Hit or Stand?'
    outcome = " "
    if in_play == True:
        outcome = "You left in the middle of a round."
        directions = "Hit deal for a new round."
        score -= 1
        in_play = False
        return
    busted = False
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    dealer_hand.add_card (deck.deal_card())
    dealer_hand.add_card (deck.deal_card())
    
    player_hand = Hand()
    player_hand.add_card (deck.deal_card())
    player_hand.add_card (deck.deal_card())
    in_play = True

def hit():
     global player_hand, in_play, busted, outcome, score, directions
     if in_play == True:
         player_hand.add_card (deck.deal_card())
         if player_hand.get_value() > 21:
             busted = True
             outcome = "Player has busted. Dealer wins."
             directions = "Hit deal for a new round."
             in_play = False 
             score -= 1
       
def stand():
    global busted, dealer_hand, score, outcome, in_play, directions
    if busted == True:
        in_play = False
        outcome = "You have already busted. Hit deal for a new round"
    elif in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
    
        if dealer_hand.get_value() > 21:
            outcome = "Dealer went bust! You win"
            directions = "Hit deal for a new round."
            in_play = False
            score += 1
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                score += 1
                in_play = False
                outcome =  "Player Wins!"
                directions = "Hit deal for a new round."
            else: 
                in_play = False
                score -= 1
                outcome = "Dealer Wins!"
                directions = "Hit deal for a new round."

def draw(canvas):
    global player_hand, outcome, directions, card_back
    canvas.draw_text("Blackjack", (475, 55), 50, 'White', 'serif')
    player_hand.draw(canvas, [10,50])
    dealer_hand.draw(canvas, [300,300])
    canvas.draw_text(outcome, (375, 130), 23,  'black', 'serif')
    canvas.draw_text(directions, (50, 250), 23,  'black', 'serif')
    if in_play == True:
        canvas.draw_image(card_back, (71/2, 96/2), (71, 96), (335.5, 348), (71, 96))
    canvas.draw_text("Score : " + str(score), (525, 95), 20, 'Yellow', 'serif')
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 700, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
dealer_hand = Hand()
player_hand = Hand()
deck = Deck()
frame.start()
directions = 'Click deal to begin game'
outcome = ' '


# Grading rubric - 18 pts total (scaled to 100)

# 1 pt - The program opens a frame with the title "Blackjack" appearing on the canvas.
# 3 pts - The program displays 3 buttons ("Deal", "Hit" and "Stand") in the control area. (1 pt per button)
# 2 pts - The program graphically displays the player's hand using card sprites. 
#		(1 pt if text is displayed in the console instead) 
# 2 pts - The program graphically displays the dealer's hand using card sprites. 
#		Displaying both of the dealer's cards face up is allowable when evaluating this bullet. 
#		(1 pt if text displayed in the console instead)
# 1 pt - Hitting the "Deal" button deals out new hands to the player and dealer.
# 1 pt - Hitting the "Hit" button deals another card to the player. 
# 1 pt - Hitting the "Stand" button deals cards to the dealer as necessary.
# 1 pt - The program correctly recognizes the player busting. 
# 1 pt - The program correctly recognizes the dealer busting. 
# 1 pt - The program correctly computes hand values and declares a winner. 
#		Evalute based on player/dealer winner messages. 
# 1 pt - The dealer's hole card is hidden until the hand is over when it is then displayed.
# 2 pts - The program accurately prompts the player for an action with the messages 
#        "Hit or stand?" and "New deal?". (1 pt per message)
# 1 pt - The program keeps score correctly.