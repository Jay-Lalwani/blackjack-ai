import os
import random
import time
import sys
sys.setrecursionlimit(20000)

#Type Number of Decks followed by 'count' to enable Griffin Ultimate Card Counting ex. for 4 decks with card count --> '4count'
#Deck is replenished and shuffled when less than a quarter of the cards remain
strategyReg = {4: 'hhhhhhhhhh', 5: 'hhhhhhhhhh', 6: 'hhhhhhhhhh', 7: 'hhhhhhhhhh', 8: 'hhhhhhhhhh', 9: 'hddddhhhhh', 10: 'ddddddddhh', 11: 'dddddddddh', 12: 'hhssshhhhh', 13: 'ssssshhhhh', 14: 'ssssshhhhh', 15: 'ssssshhhhh', 16: 'ssssshhhhh', 17: 'ssssssssss', 18: 'ssssssssss', 19: 'ssssssssss', 20: 'ssssssssss', 21: 'ssssssssss'}
#if len(value) == 1, choose value[0],  val[0 - 8] = 2 - 10, J, Q, K; val[9] = A  ;;-- > val[total([dealer_hand[0]]) - 2]
strategyAce = {12: 'hhhhhhhhhh',13: 'hhhddhhhhh', 14: 'hhhddhhhhh', 15: 'hhdddhhhhh', 16: 'hhdddhhhhh', 17: 'hddddhhhhh', 18: 'sddddsshhh', 19: 'ssssssssss', 20: 'ssssssssss', 21: 'ssssssssss'}
strategyPair = {4: 'hhpppphhhh', 6: 'hhpppphhhh', 8: 'hhhhhhhhhh', 10: 'ddddddddhh', 12: 'hpppphhhhh', 14: 'pppppphhhh', 16: 'pppppppppp', 18: 'pppppsppss', 20: 'ssssssssss', 22: 'pppppppppp'}
bankroll = {-2: 5, -1: 5, 0: 5, 1: 5, 2: 25, 3: 50, 4: 50}
deviations = 0
insuranceWins = 0
reshuffleCount = 0
#decks = input("Enter number of decks to use: ")
decks = '6count'
cardCount = False
if decks[1:] == 'count':
    cardCount = True
    decks = decks[0]
# user chooses number of decks of cards to use
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(int(decks)*4)
random.shuffle(deck)
# initialize scores
wins = 0
losses = 0

profit = 0
#initialize card count

ogCount = 0

def deal(deck):

    hand = []
    for i in range(2):
        #random.shuffle(deck)
        card = deck.pop()
        if card == 11:card = "J"
        if card == 12:card = "Q"
        if card == 13:card = "K"
        if card == 14:card = "A"
        hand.append(card)
    return hand

def play_again():
    #again = input("Do you want to play again? (Y/N) : ").lower()
    if wins + losses < 8000:
        again = 'y'
    else: again = 'n'
    if again == "y":
        game()
    else:
        #print("Bye!\n")
        print("    \033[1;32;40mWINS:  \033[1;37;40m%s   \033[1;31;40mLOSSES:  \033[1;37;40m%s\n" % (wins, losses))
        print("    \033[1;32;40mTotal Profit:  \033[1;37;40m$%s" % (profit))
        ##print(deviations)
        ##print(insuranceWins)
        exit()

def total(hand):
    total = 0
    aceCount = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total+= 10
        elif card == "A":
            total+= 11
            aceCount += 1
        else: total += card
    for a in range(aceCount):
        if total > 21:
            total -= 10
    return total

def hit(hand):
    card = deck.pop()
    if card == 11:card = "J"
    if card == 12:card = "Q"
    if card == 13:card = "K"
    if card == 14:card = "A"
    hand.append(card)
    return hand

def clear():
    if os.name == 'nt':
        os.system('CLS')
    if os.name == 'posix':
        os.system('clear')

#def #print_results(dealer_hand, player_hand):
    #clear()
    
    '''#print("\n    WELCOME TO BLACKJACK!\n")
    #print("-"*30+"\n")
    #print("    \033[1;32;40mWINS:  \033[1;37;40m%s   \033[1;31;40mLOSSES:  \033[1;37;40m%s\n" % (wins, losses))
    #print("-"*30+"\n")'''
    #print ("The dealer has a " + str(dealer_hand) + " for a total of " + str(total(dealer_hand)))
    #print ("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))

def updateCount(cardsSeen):
    
    global ogCount
    ogCardCountDic = {'A': -1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, 'J': -1, 'Q': -1, 'K': -1} #Hi-Lo
    #ogCardCountDic = {'A': -1, 2: 0.5, 3: 1, 4: 1, 5: 1.5, 6: 1, 7: 0.5, 8: 0, 9: -0.5, 10: -1, 'J': -1, 'Q': -1, 'K': -1} #Halves
    #ogCardCountDic = {'A': 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 1, 7: 1, 8: 0, 9: 0, 10: -2, 'J': -2, 'Q': -2, 'K': -2} #Hi-Opt II
    #ogCardCountDic = {'A': -1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1, 8: 0, 9: 0, 10: -2, 'J': -2, 'Q': -2, 'K': -2} #UBZ 2
    #ogCardCountDic = {'A': -60, 2: 37, 3: 45, 4: 52, 5: 70, 6: 46, 7: 27, 8: 0, 9: -17, 10: -50, 'J': -50, 'Q': -50, 'K': -50} #Griffin Ultimate

    for card in cardsSeen:
        ogCount += ogCardCountDic[card]
    

def blackjack(dealer_hand, player_hand, bet):
    global wins
    global losses
    global profit
    insBet = 0
    if total(player_hand) == 21:
        if total(dealer_hand) == 21:
            #print_results(dealer_hand, player_hand)
            #print("Push. Your score is equal to the dealer. It's a tie\n")
            #print( "Hand Winnings: $0\n")
            updateCount(dealer_hand + player_hand)
            play_again()
        else:
            #print_results(dealer_hand, player_hand)
            updateCount(dealer_hand + player_hand)
            profit += int(1.5*bet)
            #print ("Congratulations! You got a Blackjack!\n")
            #print( 'Hand Winnings: ' + str(int(1.5*bet)) + "\n")
            wins += 1
            play_again()
    else:
        if dealer_hand[0] == 'A':
            #ins = input("Would you like Insurance (Y/N): ").lower()
            
            if (ogCount/(len(deck) / 52)) >= 3:
                ins = 'y'
            else: ins = 'n'
            if ins == 'y':
                insBet = bet // 2
                #print("The dealer is showing: " + str(dealer_hand))
    if total(dealer_hand) == 21:
        if insBet == 0:
            #print()
            #print_results(dealer_hand, player_hand)
            updateCount(dealer_hand + player_hand)
            profit -= bet
            #print ("Sorry, you lose. The dealer got a blackjack.\n")
            #print( 'Hand Winnings: ' + str(-1*bet) + "\n")
            losses += 1
            play_again()
        else:
            #print()
            #print_results(dealer_hand, player_hand)
            updateCount(dealer_hand + player_hand)
            profit += insBet
            #print ("Insurance. The dealer got a blackjack.\n")
            #print( 'Hand Winnings: ' + str(insBet) + "\n")
            wins += 1
            global insuranceWins
            insuranceWins += 1
            play_again()
    else:
        if insBet != 0:
            profit -= insBet
            #print("Insurance Bet Lost: $-", end = "")
            insuranceWins -= 1
            #print(insBet)
            #print()

def score(dealer_hand, player_hand, bet):
        # score function now updates to global win/loss variables
        global wins
        global losses
        global profit
        if total(player_hand) < total(dealer_hand):
            #print_results(dealer_hand, player_hand)
            #print ("Sorry. Your score isn't higher than the dealer. You lose\n")
            losses += 1
            profit -= bet
            #print( 'Hand Winnings: $' + str(-1*bet) + "\n")
        elif total(player_hand) > total(dealer_hand):
            #print_results(dealer_hand, player_hand)
            #print ("Congratulations. Your score is higher than the dealer. You win\n")
            wins += 1
            profit += bet
            #print( 'Hand Winnings: $' + str(1*bet) + "\n")
        #else:
            #print_results(dealer_hand, player_hand)
            #print("Push. Your score is equal to the dealer. It's a tie\n")
            #print( "Hand Winnings: $0\n")

def game():
    global wins
    global losses
    global profit
    global cardCount
    global ogCount
    global deviations
    global reshuffleCount
    global deck
    choice = 0
    #clear()
    #print("\n    WELCOME TO BLACKJACK!\n")
    #print("-"*30+"\n")
    #print("    \033[1;32;40mWINS:  \033[1;37;40m%s   \033[1;31;40mLOSSES:  \033[1;37;40m%s\n" % (wins, losses))
    #print("-"*30+"\n")
    #if cardCount:
        #print("    \033[1;32;40mGriffin Ultimate:  \033[1;37;40m%s" % (griffinUltimate//( (len(deck) // 52)  )))
        #print("-"*30+"\n")
        #print("    \033[1;32;40mCard Count:  \033[1;37;40m%s" % (ogCount//( (len(deck) // 52)  )))
        #print("-"*30+"\n")
    #print("    \033[1;32;40mProfit:  \033[1;37;40m$%s" % (profit))
    #print("-"*30+"\n")
    quit=False
    #bet = input('How much would you like to bet? (or [Q]uit) $')
    tC = ogCount/(len(deck) / 52) 
    tC = round(tC)
    if tC < -2:
        tC = -2
    elif tC > 4:
        tC = 4
    bet = bankroll[tC]

    
    
    if len(deck) < 12*int(decks):
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(int(decks)*4)
        random.shuffle(deck)
        reshuffleCount += 1
        ogCount = 0
    dealer_hand = deal(deck)
    player_hand = deal(deck)
    #print ("The dealer is showing a " + str(dealer_hand[0]))
    #print()
    #print ("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
    blackjack(dealer_hand, player_hand, bet)

    while not quit:

        '''if len(player_hand) == 2:
            if player_hand[0] == player_hand[1]:
                choice = input("Do you want to [H]it, [D]ouble, s[P]lit, or [S]tand: ").lower()
                
            else: choice = input("Do you want to [H]it, [D]ouble, or [S]tand: ").lower()
        else: 
            choice = input("Do you want to [H]it or [S]tand: ").lower()'''

        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            choice = strategyPair[total([player_hand[0]]) + total([player_hand[0]])][total([dealer_hand[0]]) - 2]
        elif 'A' in player_hand and total(player_hand[0:player_hand.index('A')] + player_hand[player_hand.index('A')+1:]) == (total(player_hand) - 11):
            choice = strategyAce[total(player_hand)][total([dealer_hand[0]]) - 2]
        else: choice = strategyReg[total(player_hand)][total([dealer_hand[0]]) - 2]
        

        #deviations
        p = total(player_hand)
        d = total([dealer_hand[0]])
        trueCount = ogCount/(len(deck) / 52)
        
        if p == 16:
            if d == 9:
                if trueCount >= 5:
                    choice = 's'
                    deviations += 1
            elif d== 10:
                if trueCount >= 0:
                    choice = 's'
                    deviations += 1
        elif p==15:
            if d == 10:
                if trueCount >= 4:
                    choice = 's'
                    deviations += 1
        elif p==13:
            if d==2:
                if trueCount < -1:
                    choice = 'h'
                    deviations += 1
            elif d==3:
                if trueCount < -2:
                    choice = 'h'
                    deviations += 1
        elif p==12:
            if d==2:
                if trueCount >= 4:
                    choice = 's'
                    deviations += 1
            elif d==3:
                if trueCount >= 2:
                    choice = 's'
                    deviations += 1
            elif d==4:
                if trueCount >= 0:
                    choice = 's'
                    deviations += 1
            elif d==5:
                if trueCount < -1:
                    choice = 'h'
                    deviations += 1
            elif d==6:
                if trueCount < -1:
                    choice = 'h'
                    deviations += 1
        elif p==11:
            if d==11:
                if trueCount >= 1:
                    choice = 'd'
                    deviations += 1
        elif p==10:
            if d==10:
                if trueCount >= 4:
                    choice = 'd'
                    deviations += 1
            elif d==11:
                if trueCount >= 4:
                    choice = 'd'
                    deviations += 1

        elif p==9:
            if d==2:
                if trueCount >= 1:
                    choice = 'd'
                    deviations += 1
            elif d==7:
                if trueCount >= 4:
                    choice = 'd'
                    deviations += 1
        elif total([player_hand[0]]) == total([player_hand[1]]) == 10:
            if len(player_hand) == 2:
                if d==5:
                    if trueCount >= 5:
                        choice = 'p'
                        deviations += 1
                elif d==6:
                    if trueCount >= 5:
                        choice = 'p'
                        deviations += 1



        if len(player_hand) > 2 and choice == 'd':
            choice = 'h'

        if choice == 'h':
            hit(player_hand)
            #print(player_hand)
            #print("Hand total: " + str(total(player_hand)))
            if total(player_hand)>21:
                #print('You busted\n')
                losses += 1
                profit -= bet
                #print( 'Hand Winnings: $' + str(-1*bet) + "\n")
                updateCount(dealer_hand + player_hand)
                play_again()
        elif choice == 'd':
            #print('Doubled')
            bet = 2*bet
            hit(player_hand)
            #print(player_hand)
            #print("Hand total: " + str(total(player_hand)))
            if total(player_hand)>21:
                #print('You busted\n')
                losses += 1
                profit -= bet
                #print( 'Hand Winnings: $' + str(-1*bet) + "\n")
                updateCount(dealer_hand + player_hand)
                play_again()
            else:
                while total(dealer_hand)<17:
                    hit(dealer_hand)
                    #print(dealer_hand)
                    if total(dealer_hand)>21:
                        #print('Dealer busts, you win!\n')
                        wins += 1
                        profit += bet
                        #print( 'Hand Winnings: $' + str(1*bet) + "\n")
                        updateCount(dealer_hand + player_hand)
                        play_again()
                score(dealer_hand,player_hand, bet)
                updateCount(dealer_hand + player_hand)
                play_again()
        elif choice=='s':
            while total(dealer_hand)<17:
                hit(dealer_hand)
                #print(dealer_hand)
                if total(dealer_hand)>21:
                    #print('Dealer busts, you win!\n')
                    wins += 1
                    profit += bet
                    #print( 'Hand Winnings: $' + str(1*bet) + "\n")
                    updateCount(dealer_hand + player_hand)
                    play_again()
            score(dealer_hand,player_hand, bet)
            updateCount(dealer_hand + player_hand)
            play_again()
        elif choice=='p':
            player_hand1 = [player_hand[0]]
            player_hand2 = [player_hand[1]]
            hit(player_hand1)
            hit(player_hand2)
            #print()
            #print ("You have a " + str(player_hand1) + " for a total of " + str(total(player_hand1)) + " on Hand 1")
            while True:
                #choice = input("Do you want to [H]it or [S]tand Hand 1: ").lower()
                
                if 'A' in player_hand and total(player_hand[0:player_hand.index('A')] + player_hand[player_hand.index('A')+1:]) == (total(player_hand) - 11):
                    choice = strategyAce[total(player_hand)][total([dealer_hand[0]]) - 2]
                else: choice = strategyReg[total(player_hand)][total([dealer_hand[0]]) - 2]

                if choice == 'h' or choice == 'd':
                    hit(player_hand1)
                    #print(player_hand1)
                    #print("Hand 1 total: " + str(total(player_hand1)))
                    if total(player_hand1)>21:
                        #print('You busted on Hand 1\n')
                        losses += 1
                        profit -= bet
                        
                        #print ("You have a " + str(player_hand2) + " for a total of " + str(total(player_hand2)) + " on Hand 2")
                        while True:
                            
                            #choice = input("Do you want to [H]it or [S]tand Hand 2: ").lower()

                            if 'A' in player_hand and total(player_hand[0:player_hand.index('A')] + player_hand[player_hand.index('A')+1:]) == (total(player_hand) - 11):
                                choice = strategyAce[total(player_hand)][total([dealer_hand[0]]) - 2]
                            else: choice = strategyReg[total(player_hand)][total([dealer_hand[0]]) - 2]

                            if choice == 'h' or choice == 'd':
                                hit(player_hand2)
                                #print(player_hand2)
                                #print("Hand 2 total: " + str(total(player_hand2)))
                                if total(player_hand2)>21:
                                    #print('You busted on Hand 2\n')
                                    losses += 1
                                    profit -= bet
                                    #print( 'Both Hand Winnings: $' + str(-2*bet) + "\n")
                                    updateCount(dealer_hand + player_hand1 + player_hand2)
                                    play_again()
                            elif choice=='s':
                                while total(dealer_hand)<17:
                                    hit(dealer_hand)
                                    #print(dealer_hand)
                                    if total(dealer_hand)>21:
                                        #print('Dealer busts, you win Hand 2!\n')
                                        wins += 1
                                        profit += 1*bet
                                        #print( 'Hand Winnings: $' + '0' + "\n")
                                        updateCount(dealer_hand + player_hand)
                                        play_again()
                                #print("For Hand 2:", end = " ")
                                score(dealer_hand,player_hand2, bet)
                                updateCount(dealer_hand + player_hand1 + player_hand2)
                                play_again()
                elif choice=='s':
                    #print()
                    #print ("You have a " + str(player_hand2) + " for a total of " + str(total(player_hand2)) + " on Hand 2")
                    while True:
                        #choice = input("Do you want to [H]it or [S]tand Hand 2: ").lower()

                        if 'A' in player_hand and total(player_hand[0:player_hand.index('A')] + player_hand[player_hand.index('A')+1:]) == (total(player_hand) - 11):
                            choice = strategyAce[total(player_hand)][total([dealer_hand[0]]) - 2]
                        else: choice = strategyReg[total(player_hand)][total([dealer_hand[0]]) - 2]

                        if choice == 'h' or choice == 'd':
                            hit(player_hand2)
                            #print(player_hand2)
                            #print("Hand 2 total: " + str(total(player_hand2)))
                            if total(player_hand2)>21:
                                #print('You busted on Hand 2\n')
                                losses += 1
                                profit -= bet
                                while total(dealer_hand)<17:
                                    hit(dealer_hand)
                                    #print(dealer_hand)
                                    if total(dealer_hand)>21:
                                        #print('Dealer busts, you win Hand 1!\n')
                                        wins += 1
                                        profit += bet
                                        #print( 'Hand Winnings: $' + '0' + "\n")
                                        updateCount(dealer_hand + player_hand1 + player_hand2)
                                        play_again()
                                score(dealer_hand,player_hand1, bet)
                                updateCount(dealer_hand + player_hand1 + player_hand2)
                                play_again()
                        elif choice=='s':
                            while total(dealer_hand)<17:
                                hit(dealer_hand)
                                #print(dealer_hand)
                                if total(dealer_hand)>21:
                                    #print('Dealer busts, you win Both Hands!\n')
                                    wins += 2
                                    profit += 2*bet
                                    #print( 'Both Hand Winnings: $' + str(2*bet) + "\n")
                                    updateCount(dealer_hand + player_hand)
                                    play_again()
                            #print()
                            #print("For Hand 1:", end= " ")
                            score(dealer_hand,player_hand1, bet)
                            #print()
                            #print("For Hand 2:", end= " ")
                            score(dealer_hand,player_hand2, bet)
                            updateCount(dealer_hand + player_hand1 + player_hand2)
                            play_again()
if __name__ == "__main__":
   for i in range(1000):
    game()
    #print(profit)
