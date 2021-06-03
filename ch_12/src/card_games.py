"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
from __future__ import annotations
import abc
import collections
import random
from enum import Enum, auto
from typing import (
    Any,
    Counter,
    Iterator,
    Iterable,
    List,
    NamedTuple,
    TypeVar,
    cast,
)


class Suit(str, Enum):
    Clubs = "\N{Black Club Suit}"
    Diamonds = "\N{Black Diamond Suit}"
    Hearts = "\N{Black Heart Suit}"
    Spades = "\N{Black Spade Suit}"


class Card(NamedTuple):
    """
    >>> c = Card(5, Suit.Spades)
    >>> print(c)
    5♠
    >>> c
    Card(rank=5, suit=<Suit.Spades: '♠'>)

    """

    rank: int
    suit: Suit

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class Trick(int, Enum):
    pass


class Hand(List[Card]):
    def __init__(self, *cards: Card) -> None:
        super().__init__(cards)

    def scoring(self) -> list[Trick]:
        pass


class CardGameFactory(abc.ABC):
    @abc.abstractmethod
    def make_card(self, rank: int, suit: Suit) -> "Card":
        ...

    @abc.abstractmethod
    def make_hand(self, *cards: Card) -> "Hand":
        ...


class CribbageCard(Card):
    @property
    def points(self) -> int:
        return self.rank


class CribbageAce(Card):
    @property
    def points(self) -> int:
        return 1


class CribbageFace(Card):
    @property
    def points(self) -> int:
        return 10


class CribbageTrick(Trick):
    Fifteen = auto()
    Pair = auto()
    Run_3 = auto()
    Run_4 = auto()
    Run_5 = auto()
    Right_Jack = auto()


import itertools

C = TypeVar("C")


def powerset(iterable: Iterable[C]) -> Iterator[tuple[C, ...]]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


class CribbageHand(Hand):
    starter: Card

    def upcard(self, starter: Card) -> "Hand":
        self.starter = starter
        return self

    def scoring(self) -> list[Trick]:
        """15's. Pairs. Runs. Right Jack."""

        def trick_iter(cards: list[CribbageCard]) -> Iterator[Trick]:
            for subset in powerset(cards):
                if sum(c.points for c in subset) == 15:
                    yield CribbageTrick.Fifteen
            for c1, c2 in itertools.combinations(cards, 2):
                if c1.rank == c2.rank:
                    yield CribbageTrick.Pair

        def run_length(sorted_cards: list[CribbageCard]) -> int:
            card_iter = iter(sorted_cards)
            base = next(card_iter)
            for offset, card in enumerate(card_iter, start=1):
                if base.rank + offset != card.rank:
                    break
            return offset + 1

        hand_plus_starter = cast(List[CribbageCard], self + [self.starter])
        hand_plus_starter.sort()
        tricks = list(trick_iter(hand_plus_starter))
        if run_length(hand_plus_starter) == 5:
            tricks += [CribbageTrick.Run_5]
        elif (
            run_length(hand_plus_starter) == 4 or run_length(hand_plus_starter[1:]) == 4
        ):
            tricks += [CribbageTrick.Run_4]
        elif (
            run_length(hand_plus_starter) == 3
            or run_length(hand_plus_starter[1:]) == 3
            or run_length(hand_plus_starter[2:]) == 3
        ):
            tricks += [CribbageTrick.Run_3]
        right_jack = any(c.rank == 11 and c.suit == self.starter.suit for c in self)
        if right_jack:
            tricks += [CribbageTrick.Right_Jack]
        return tricks


class CribbageFactory(CardGameFactory):
    def make_card(self, rank: int, suit: Suit) -> "Card":
        if rank == 1:
            return CribbageAce(rank, suit)
        elif 2 <= rank < 11:
            return CribbageCard(rank, suit)
        else:
            return CribbageFace(rank, suit)

    def make_hand(self, *cards: Card) -> "Hand":
        return CribbageHand(*cards)


test_cribbage = """
>>> factory = CribbageFactory()
>>> cards = [
...     factory.make_card(6, Suit.Clubs),
...     factory.make_card(7, Suit.Diamonds),
...     factory.make_card(8, Suit.Hearts),
...     factory.make_card(9, Suit.Spades),
... ]
>>> starter = factory.make_card(5, Suit.Spades)
>>> hand = factory.make_hand(*cards)
>>> score = sorted(hand.upcard(starter).scoring())
>>> [t.name for t in score]
['Fifteen', 'Fifteen', 'Run_5']

"""


class PokerCard(Card):
    def __str__(self) -> str:
        if self.rank == 14:
            return f"A{self.suit}"
        return f"{self.rank}{self.suit}"


class PokerTrick(Trick):
    Pair = auto()
    TwoPair = auto()
    Three = auto()
    Straight = auto()
    Flush = auto()
    FullHouse = auto()
    Four = auto()
    StraightFlush = auto()


class PokerHand(Hand):
    def scoring(self) -> list[Trick]:
        """Return a single 'Trick'"""
        # Distinct Ranks
        ranks: Counter[int] = collections.Counter(c.rank for c in self)
        # Distinct Suits
        flush = len(set(c.suit for c in self)) == 1
        if len(ranks) == 1:
            # five of a kind!
            raise Exception(f"Broken Hand {self}")
        elif len(ranks) == 2:
            # 4-1 or 3-2.
            card, count = ranks.most_common(1)[0]
            if count == 4:
                return [PokerTrick.Four]
            elif count == 3:
                return [PokerTrick.FullHouse]
            else:
                raise Exception(f"Broken Hand {self}")
        elif len(ranks) == 3:
            # 3-1-1, or 2-2-1
            card, count = ranks.most_common(1)[0]
            if count == 3:
                return [PokerTrick.Three]
            elif count == 2:
                return [PokerTrick.TwoPair]
            else:
                raise Exception(f"Broken Hand {self}")
        elif len(ranks) == 4:
            # 2-1-1-1
            return [PokerTrick.Pair]
        elif len(ranks) == 5:
            # straight?
            base = min(ranks)
            straight = all(base + offset == rank for offset, rank in enumerate(ranks))
            # straight flush?
            if straight and flush:
                return [PokerTrick.StraightFlush]
            elif straight:
                return [PokerTrick.Straight]
            elif flush:
                return [PokerTrick.Flush]
            else:
                return []
        else:
            return []


class PokerFactory(CardGameFactory):
    def make_card(self, rank: int, suit: Suit) -> "Card":
        if rank == 1:
            # Aces above kings
            rank = 14
        return PokerCard(rank, suit)

    def make_hand(self, *cards: Card) -> "Hand":
        return PokerHand(*cards)


test_poker = """
>>> factory = PokerFactory()
>>> cards = [
...     factory.make_card(5, Suit.Clubs),
...     factory.make_card(5, Suit.Diamonds),
...     factory.make_card(5, Suit.Hearts),
...     factory.make_card(6, Suit.Spades),
...     factory.make_card(6, Suit.Spades),
... ]
>>> hand = factory.make_hand(*cards)
>>> hand.scoring()
[<PokerTrick.FullHouse: 6>]

"""


class Game:
    def __init__(self, factory: CardGameFactory) -> None:
        self.factory = factory

    def prepare(self) -> None:
        self.deck = [
            self.factory.make_card(r, s) for r in range(1, 14) for s in iter(Suit)
        ]
        random.shuffle(self.deck)

    def deal(self) -> Hand:
        hand = self.factory.make_hand(*self.deck[:5])
        return hand

    def score(self, hand: Hand) -> None:
        print(hand.scoring())


class Poker(Game):
    pass


class Cribbage(Game):
    def score(self, hand: Hand) -> None:
        up_card = self.deck[5]
        hand = cast(CribbageHand, hand).upcard(up_card)
        print(hand.scoring())


from typing import Protocol


class CardGameFactoryProtocol(Protocol):
    def make_card(self, rank: int, suit: Suit) -> "Card":
        ...

    def make_hand(self, *cards: Card) -> "Hand":
        ...


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
