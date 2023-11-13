import random
import matplotlib.pyplot as plt
random.seed(619)

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
COLORS = ['Red', 'Black']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

#useful functions
def isSubArray(array, subarray):
        n = len(array)
        m = len(subarray)
    
        for i in range(n - m + 1):
            for j in range(m):
                if array[i + j] != subarray[j]:
                    break
            else:  
                return True
    
        return False

def prime_number(n):
    for i in range(2, n//2+1):
        if (n % i) == 0:
            return False
    return True

def rank_to_number(rank):
    rank_values = {
        'Ace' : 1,
        'Jack' : 11,
        'Queen' : 12,
        'King' : 13
    }
    if rank.isdigit():
        return int(rank)
    else:
        return rank_values[rank]
    
def is_palindrome(num):
        num_str = str(num)
        return num_str == num_str[::-1]


#classes
class DeckDealer:
    def __init__(self):
        self.deck = self.generate_deck()

    def generate_deck(self):
        deck = []
        for suit in SUITS:
            for color in COLORS:
                for rank in RANKS:
                    card = {
                        'suit': suit,
                        'color': color,
                        'rank': rank
                    }
                    card['color'] = 'Red' if card['suit'] in ['Diamonds', 'Hearts'] else 'Black'
                    deck.append(card)
        return deck
    
    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_cards(self, number_of_cards):
        drawn_cards = random.sample(self.deck, number_of_cards)
        return drawn_cards


class Games:
    def __init__(self, deck_dealer):
        self.deck_dealer = deck_dealer
    
    def sahara_ace(self):
        card = self.deck_dealer.draw_cards(1)[0]
        if(card['rank']=='Ace'):
            return 10
        else:
            return 0
        
    def Tunisian_Twins(self):
        cards = self.deck_dealer.draw_cards(2)
        
        first_card = cards[0]
        second_card = cards[1]
        if (first_card['rank']==second_card['rank'] or first_card['color'] == second_card['color'] or first_card['suit']==second_card['suit']):
            return 50
        else:
            return 0

    def medina_beggie(self):
        cards = self.deck_dealer.draw_cards(2)
        
        first_card = cards[0]
        second_card = cards[1]

        if RANKS.index(first_card["rank"]) < RANKS.index(second_card["rank"]):
            return 2
        else:
            return 0
        
    def desert_hearts(self): 
        cards = self.deck_dealer.draw_cards(3)
    
        heart_score = sum(1 for card in cards if card["suit"] == "Hearts")

        return heart_score

    def oasis_runny(self):
        cards = self.deck_dealer.draw_cards(5)
        cards.sort(key=lambda x: RANKS.index(x['rank']))
        cards_ranks = [card['rank'] for card in cards]
        if isSubArray(RANKS,cards_ranks):
            return 5
        else:
            return 0

#ribat_links is a game where the player draw 4 cards and if the sum of their ranks multiplied by the lowest rank is a palindrome number he wins 10 dinars else he loses. 
    def ribat_links(self):
        cards = self.deck_dealer.draw_cards(4)

        ranks = [rank_to_number(card['rank']) for card in cards]
        sum_of_ranks = sum(ranks)
        lowest_rank = min(ranks)

        if is_palindrome(sum_of_ranks * lowest_rank):
            return 10
        else:
            return 0
        
        
#monte carlo simulation 
def monte_carlo(simulation_nbr):
    best_game = ""
    highest_probability = 0

    the_games = {
        "Sahara Ace": games.sahara_ace,
        "Tunisian Twins": games.Tunisian_Twins,
        "Medina Biggie": games.medina_beggie,
        "Desert Hearts": games.desert_hearts,
        "Oasis Runny": games.oasis_runny,
        "Ribat Links": games.ribat_links
    }

    print("Game\t\t\tProbability\tWins\t\tExpected Winnings")
    print("-" * 74)

    for game_name, game_function in the_games.items():
        nbr_wins = 0
        total_winnings = 0
        
        for i in range(simulation_nbr):
            winning = game_function()
            if winning>0:
                nbr_wins += 1
            total_winnings += winning

        probability_of_winning = nbr_wins / simulation_nbr
        expected_winnings_per_play = total_winnings

        if probability_of_winning > highest_probability:
            best_game = game_name
            highest_probability = probability_of_winning

        print(f"{game_name.ljust(20)}\t{probability_of_winning*100:.2f}%\t\t{nbr_wins}\t\t{expected_winnings_per_play:} TND")
    print(f"\nThe best game to deploy is '{best_game}' with a winning probability of {highest_probability*100:.2f}%\n")
    
    return probabilities

#instanciation & Testing Results
deck_dealer = DeckDealer()
deck_dealer.shuffle_deck()
games = Games(deck_dealer)

#results charts
def plot_results(probabilities):
    games = list(probabilities.keys())
    probs = list(probabilities.values())

    plt.figure(figsize=(10, 6))
    plt.bar(games, probs, color='purple')
    plt.xlabel('Game Names')
    plt.ylabel('Winning Probability')
    plt.title('Winning Probability for Each Game')
    plt.ylim(0, 1)
    plt.show()

#get probabilities
def get_probabilities(simulation_nbr):
    probabilities = {}
    the_games = {
        "Sahara Ace": games.sahara_ace,
        "Tunisian Twins": games.Tunisian_Twins,
        "Medina Biggie": games.medina_beggie,
        "Desert Hearts": games.desert_hearts,
        "Oasis Runny": games.oasis_runny,
        "Ribat Links": games.ribat_links
    }

    for game_name, game_function in the_games.items():
        nbr_wins = 0

        for i in range(simulation_nbr):
            winning = game_function()
            if winning > 0:
                nbr_wins += 1

        probability_of_winning = nbr_wins / simulation_nbr
        probabilities[game_name] = probability_of_winning

    return probabilities    

#showing results
simulation_nbr = 100000
probabilities = get_probabilities(simulation_nbr)
monte_carlo(simulation_nbr)
plot_results(probabilities)
