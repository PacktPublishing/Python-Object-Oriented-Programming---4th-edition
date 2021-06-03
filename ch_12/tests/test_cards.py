"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
from pytest import *
import card_games

def test_cribbage_hand():
    factory = card_games.CribbageFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(5, card_games.Suit.Diamonds),
        factory.make_card(5, card_games.Suit.Hearts),
        factory.make_card(11, card_games.Suit.Spades),
    ]
    starter = factory.make_card(5, card_games.Suit.Spades)
    hand = factory.make_hand(*cards)
    actual = sorted(hand.upcard(starter).scoring())
    assert actual == [
        card_games.CribbageTrick.Fifteen,
        card_games.CribbageTrick.Fifteen,
        card_games.CribbageTrick.Fifteen,
        card_games.CribbageTrick.Fifteen,
        card_games.CribbageTrick.Fifteen,
        card_games.CribbageTrick.Fifteen,
        card_games.CribbageTrick.Fifteen,
        card_games.CribbageTrick.Fifteen,
        card_games.CribbageTrick.Pair,
        card_games.CribbageTrick.Pair,
        card_games.CribbageTrick.Pair,
        card_games.CribbageTrick.Pair,
        card_games.CribbageTrick.Pair,
        card_games.CribbageTrick.Pair,
        card_games.CribbageTrick.Right_Jack,
    ]

def test_poker_hand_sf():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(6, card_games.Suit.Clubs),
        factory.make_card(7, card_games.Suit.Clubs),
        factory.make_card(8, card_games.Suit.Clubs),
        factory.make_card(9, card_games.Suit.Clubs),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == [card_games.PokerTrick.StraightFlush]

def test_poker_hand_4():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(5, card_games.Suit.Diamonds),
        factory.make_card(5, card_games.Suit.Hearts),
        factory.make_card(5, card_games.Suit.Spades),
        factory.make_card(6, card_games.Suit.Spades),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == [card_games.PokerTrick.Four]

def test_poker_hand_fh():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(5, card_games.Suit.Diamonds),
        factory.make_card(5, card_games.Suit.Hearts),
        factory.make_card(6, card_games.Suit.Spades),
        factory.make_card(6, card_games.Suit.Spades),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == [card_games.PokerTrick.FullHouse]

def test_poker_hand_flush():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(6, card_games.Suit.Clubs),
        factory.make_card(7, card_games.Suit.Clubs),
        factory.make_card(8, card_games.Suit.Clubs),
        factory.make_card(10, card_games.Suit.Clubs),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == [card_games.PokerTrick.Flush]

def test_poker_hand_straight():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(6, card_games.Suit.Clubs),
        factory.make_card(7, card_games.Suit.Clubs),
        factory.make_card(8, card_games.Suit.Clubs),
        factory.make_card(10, card_games.Suit.Clubs),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == [card_games.PokerTrick.Flush]

def test_poker_hand_3():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(5, card_games.Suit.Diamonds),
        factory.make_card(5, card_games.Suit.Hearts),
        factory.make_card(6, card_games.Suit.Spades),
        factory.make_card(7, card_games.Suit.Spades),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == [card_games.PokerTrick.Three]

def test_poker_hand_22():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(5, card_games.Suit.Diamonds),
        factory.make_card(6, card_games.Suit.Hearts),
        factory.make_card(6, card_games.Suit.Spades),
        factory.make_card(7, card_games.Suit.Spades),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == [card_games.PokerTrick.TwoPair]

def test_poker_hand_2():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(5, card_games.Suit.Clubs),
        factory.make_card(5, card_games.Suit.Diamonds),
        factory.make_card(6, card_games.Suit.Hearts),
        factory.make_card(7, card_games.Suit.Spades),
        factory.make_card(8, card_games.Suit.Clubs),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == [card_games.PokerTrick.Pair]

def test_poker_hand_nothing():
    factory = card_games.PokerFactory()
    cards = [
        factory.make_card(3, card_games.Suit.Clubs),
        factory.make_card(5, card_games.Suit.Diamonds),
        factory.make_card(7, card_games.Suit.Hearts),
        factory.make_card(9, card_games.Suit.Spades),
        factory.make_card(11, card_games.Suit.Clubs),
    ]
    hand = factory.make_hand(*cards)
    assert hand.scoring() == []
