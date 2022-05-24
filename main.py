from datastore import SuperheroDB
from game import Card
import random

super_heros = SuperheroDB()

# establish all possible cards
max_cards = super_heros.get_last_superhero_id()
all_cards = list(range(1, max_cards + 1))
random.shuffle(all_cards)

# create game pack
pack_size = 10
pack = []
index = 0
while len(pack) < pack_size:
    card = Card(super_heros.get_card_details(all_cards[index]))
    if not card.all_blank():
        pack.append(card)
    index += 1

# establish ranking
for card in pack:
    card.get_rankings(pack)
    
# deal cards
player_hand = []
ai_hand = []

while len(pack) > 0:
    player_hand.append(pack.pop(0))
    ai_hand.append(pack.pop(0))
    
# display cards
print("Player Hand")
for card in player_hand:
    card.show_card_details()
    
print("AI Hand")
for card in ai_hand:
    card.show_card_details()
