import random

# Constants
SUITS = ['♠', '♦', '♣', '♥']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
DECKS = 6
MIN_BET = 10
MAX_BET = 1000

# Function to create a deck
def create_deck():
    deck = []
    for _ in range(DECKS):
        for suit in SUITS:
            for rank in RANKS:
                deck.append((rank, suit))
    random.shuffle(deck)
    return deck

# Function to deal a card
def deal_card(deck):
    return deck.pop()

# Function to calculate hand value
def calc_hand_val(hand):
    value = sum(VALUES[card[0]] for card in hand)
    num_aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

# Function to display cards in card shapes
def show_cards(hand, hide_second_card=False):
    lines = ["", "", ""]
    for i, card in enumerate(hand):
        rank, suit = card
        if hide_second_card and i == 1:
            lines[0] += "┌─────┐ "
            lines[1] += "│  ?  │ "
            lines[2] += "└─────┘ "
        else:
            val = f"{rank}{suit}".ljust(3)
            lines[0] += "┌─────┐ "
            lines[1] += f"│ {val} │ "
            lines[2] += "└─────┘ "
    return '\n'.join(lines)

# Function to check if deck needs shuffling
def check_shuffle(deck):
    if len(deck) < 0.25 * DECKS * len(SUITS) * len(RANKS):
        print("\nShuffling the deck... 🏁🏁🏁\n")
        deck = create_deck()
        print("Deck shuffled!")
    return deck

# Welcome message and rules
def welcome_message():
    print("Welcome to Blackjack!")
    print("Rules:")
    print("1. Game is played with 6 decks.")
    print("2. Up to 4 players can play against the dealer.")
    print("3. Each player starts with an opening balance.")
    print(f"4. Bets must be between ${MIN_BET} and ${MAX_BET}.")
    print("5. Cards have face values. J/Q/K = 10, A = 1 or 11.")
    print("6. If 75% of the cards are used, deck will shuffle.\n")

# Main game function
def play_blackjack():
    welcome_message()
    deck = create_deck()
    num_players = int(input("How many players are going to play against the dealer? (1-4): "))
    players = []
    for i in range(num_players):
        name = input(f"Enter name for player {i+1}: ")
        balance = int(input(f"Enter opening balance for {name}: "))
        players.append({'name': name, 'balance': balance, 'hand': [], 'bet': 0, 'wins': 0, 'losses': 0, 'active': True})

    dealer_hand = []
    round_num = 1
    while any(player['active'] for player in players):
        print(f"\nRound: {round_num}")
        round_num += 1

        for player in players:
            if not player['active']:
                continue
            print(f"{player['name']}'s balance: ${player['balance']}")
            bet = int(input(f"{player['name']}, how much do you want to bet? (Min: $10, Max: $1000): "))
            while bet < MIN_BET or bet > MAX_BET or bet > player['balance']:
                bet = int(input(f"Invalid bet. {player['name']}, how much do you want to bet? (Min: $10, Max: $1000): "))
            player['bet'] = bet
            player['balance'] -= bet

        for player in players:
            if player['active']:
                player['hand'] = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]

        print("\nDealer's hand:")
        print(show_cards(dealer_hand, hide_second_card=True))

        for player in players:
            if player['active']:
                print(f"\n{player['name']}'s hand:")
                print(show_cards(player['hand']))
                print(f"Your total: {calc_hand_val(player['hand'])}")

        for player in players:
            if not player['active']:
                continue
            while calc_hand_val(player['hand']) < 21:
                action = input(f"{player['name']}, do you want to hit or stand? (h/s): ").lower()
                if action == 'h':
                    player['hand'].append(deal_card(deck))
                    print(show_cards(player['hand']))
                    print(f"New total: {calc_hand_val(player['hand'])}")
                else:
                    break

        while calc_hand_val(dealer_hand) < 17:
            dealer_hand.append(deal_card(deck))

        print("\nDealer's hand:")
        print(show_cards(dealer_hand))
        print(f"Dealer's total: {calc_hand_val(dealer_hand)}")

        dealer_value = calc_hand_val(dealer_hand)
        for player in players:
            if not player['active']:
                continue
            player_value = calc_hand_val(player['hand'])
            if player_value > 21:
                print(f"{player['name']} busts! Dealer wins.")
                player['losses'] += 1
            elif dealer_value > 21 or player_value > dealer_value:
                print(f"{player['name']} wins! {player['name']} wins ${2 * player['bet']}.")
                player['balance'] += 2 * player['bet']
                player['wins'] += 1
            elif player_value == dealer_value:
                print(f"{player['name']} ties with the dealer. Bet returned.")
                player['balance'] += player['bet']
            else:
                print(f"Dealer wins against {player['name']}.")
                player['losses'] += 1

        deck = check_shuffle(deck)

        # Ask each player if they want to continue
        for player in players:
            if player['active']:
                cont = input(f"{player['name']}, do you want to continue playing? (y/n): ").lower()
                if cont != 'y':
                    player['active'] = False
                    print(f"\nThanks for playing, {player['name']}!")
                    print(f"Final Balance: ${player['balance']} | Wins: {player['wins']} | Losses: {player['losses']}\n")

    print("\nGame over! Final results:")
    for player in players:
        print(f"{player['name']} - Final Balance: ${player['balance']} | Wins: {player['wins']} | Losses: {player['losses']}")

# Run the game
play_blackjack()