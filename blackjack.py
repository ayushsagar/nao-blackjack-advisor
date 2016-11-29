# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from naoqi import *
import time


class Cards():
    cardValue = {
                'spades2': 2,
                'spades3': 3,
                'spades4': 4,
                'spades5': 5,
                'spades6': 6,
                'spades7': 7,
                'spades8': 8,
                'spades9': 9,
                'spades10': 10,
                'spadesJ': 10,
                'spadesQ': 10,
                'spadesK': 10,
                'spadesA': 1,
    
                'hearts2': 2,
                'hearts3': 3,
                'hearts4': 4,
                'hearts5': 5,
                'hearts6': 6,
                'hearts7': 7,
                'hearts8': 8,
                'hearts9': 9,
                'hearts10': 10,
                'heartsJ': 10,
                'heartsQ': 10,
                'heartsK': 10,
                'heartsA': 1,
    
                'clubs2': 2,
                'clubs3': 3,
                'clubs4': 4,
                'clubs5': 5,
                'clubs6': 6,
                'clubs7': 7,
                'clubs8': 8,
                'clubs9': 9,
                'clubs10': 10,
                'clubsJ': 10,
                'clubsQ': 10,
                'clubsK': 10,
                'clubsA': 1,
    
                'diamonds2': 2,
                'diamonds3': 3,
                'diamonds4': 4,
                'diamonds5': 5,
                'diamonds6': 6,
                'diamonds7': 7,
                'diamonds8': 8,
                'diamonds9': 9,
                'diamonds10': 10,
                'diamondsJ': 10,
                'diamondsQ': 10,
                'diamondsK': 10,
                'diamondsA': 1
                }

    def __init__(self):

        self.cardState = {
                    'spades2': False,
                    'spades3': False,
                    'spades4': False,
                    'spades5': False,
                    'spades6': False,
                    'spades7': False,
                    'spades8': False,
                    'spades9': False,
                    'spades10': False,
                    'spadesJ': False,
                    'spadesQ': False,
                    'spadesK': False,
                    'spadesA': False,
        

                    'hearts2': False,
                    'hearts3': False,
                    'hearts4': False,
                    'hearts5': False,
                    'hearts6': False,
                    'hearts7': False,
                    'hearts8': False,
                    'hearts9': False,
                    'hearts10': False,
                    'heartsJ': False,
                    'heartsQ': False,
                    'heartsK': False,
                    'heartsA': False,
        
                    'clubs2': False,
                    'clubs3': False,
                    'clubs4': False,
                    'clubs5': False,
                    'clubs6': False,
                    'clubs7': False,
                    'clubs8': False,
                    'clubs9': False,
                    'clubs10': False,
                    'clubsJ': False,
                    'clubsQ': False,
                    'clubsK': False,
                    'clubsA': False,
        
                    'diamonds2': False,
                    'diamonds3': False,
                    'diamonds4': False,
                    'diamonds5': False,
                    'diamonds6': False,
                    'diamonds7': False,
                    'diamonds8': False,
                    'diamonds9': False,
                    'diamonds10': False,
                    'diamondsJ': False,
                    'diamondsQ': False,
                    'diamondsK': False,
                    'diamondsA': False
                    }
        self.dealerCards = []
    def total(self):
        '''returns total value of the cards held my player'''
        val = 0
        for card in self.cardState:
            if self.cardState[card] == True:
                if card not in self.dealerCards:       #count all except dealer cards         
                    val += Cards.cardValue[card]
        return val

    def remember(self, card, isDealerCard=False):
        '''Remembers posession of the given card.
        Returns -1 if card has already been seen.
        Returns 0 if card successfully remembered.
        raises ValueError if card name is invalid'''
        try:
            if self.cardState[card] == True:
                return -1   #sends a warning that card has already been seen
            self.cardState[card] = True
            if isDealerCard:
                self.dealerCards.append(card)
        except KeyError:
            raise ValueError("invalid card")
        return 0
        
    def hitFavorable(self):
        thresh = 21 - self.total()
        favorableCardCount = 0
        for card in self.cardState:
            if Cards.cardValue[card] <= thresh and self.cardState[card] == False:
                favorableCardCount += 1

        unseenCardCount = 0
        for card in self.cardState:
            if self.cardState[card] == False:
                unseenCardCount += 1
        print "favorable cards:", favorableCardCount, " unseen cards:", unseenCardCount
        return favorableCardCount/float(unseenCardCount)

ROBOT_IP="192.168.86.176"

barcode=ALProxy("ALBarcodeReader", ROBOT_IP, 9559)
tts = ALProxy("ALTextToSpeech", ROBOT_IP, 9559)
barcode.subscribe("test_barcode")
memory=ALProxy("ALMemory", ROBOT_IP, 9559)


def listen(command):
    return None

def seeCard(cards, prompt, isDealerCard=False):
    tts.say(prompt)
    reco_card = ""
    while reco_card not in Cards.cardValue:
        data = memory.getData("BarcodeReader/BarcodeDetected")
        if data is not None and len(data) > 0:
            reco_card = data[0][0]
        else:
            reco_card = None
    cards.remember(reco_card, isDealerCard)
    return reco_card

def cardDesc(card):
    fullName = {'J':'Jack','Q':'Queen','K':'King','A':'Ace'}

    if card[-1] in ['J','Q','K','A']:
        return fullName[card[-1]] + " of " + card[:-1]

    if card[-1] == '0':
        return "10 of " + card[:-2]
        
    elif card[-1] in ['2','3','4','5','6','7','8','9']:
        return card[-1] + " of " + card[:-1]

def decision(cards):
    total = cards.total()
    hitFavorable = cards.hitFavorable()
    outputStr = "Your total is, " + str(total) + ". "
    if cards.total() < 17:
        outputStr += "You have no choice, you have to hit."
    elif hitFavorable > 0.3775:
        outputStr += "I feel, you should hit"
    else:
        outputStr += "I feel, you should stay"

    return outputStr        

cardPrompts=["show me your first card", "show me your other card", "show me the dealer's card"]

while(1):
    # Wait for "new game command"
    listen("new game")
    tts.say("okay...")

    # instantite cards
    cards = Cards()
    time.sleep(1)
    
    reco_card = seeCard(cards, "show me your first card")
    if reco_card in Cards.cardValue:
        tts.say("I see, a " + cardDesc(reco_card) + ";")

    reco_card = seeCard(cards, "show me your second card")
    if reco_card in Cards.cardValue:
        tts.say("I see, a " + cardDesc(reco_card) + ";")

    reco_card = seeCard(cards, "show me the dealer's card",isDealerCard=True)
    if reco_card in Cards.cardValue:
        tts.say("I see, a " + cardDesc(reco_card) + ";")

    tts.say(decision(cards))
    break
