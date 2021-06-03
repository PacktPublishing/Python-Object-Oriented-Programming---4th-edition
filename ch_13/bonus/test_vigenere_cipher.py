"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
import pytest
from vigenere_cipher import (
    VigenèreCipher,
    combine_character,
    separate_character,
    VigenèreCipher_2,
    VigenèreCipher_3,
)


# Version 1. Incomplete.


@pytest.fixture
def vigenere_train() -> VigenèreCipher:
    cipher = VigenèreCipher("TRAIN")
    return cipher


def test_encode(vigenere_train: VigenèreCipher) -> None:
    encoded = vigenere_train.encode("ENCODEDINPYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


@pytest.mark.xfail(reason="Fails with version 1 of VigenèreCipher")
def test_decode(vigenere_train: VigenèreCipher) -> None:
    decoded = vigenere_train.decode("XECWQXUIVCRKHWA")  # type: ignore [attr-defined]
    assert decoded == "ENCODEDINPYTHON"


@pytest.mark.xfail(reason="Fails with version 1 of VigenèreCipher")
def test_encode_character(vigenere_train: VigenèreCipher) -> None:
    encoded = vigenere_train.encode("E")
    assert encoded == "X"


def test_encode_spaces(vigenere_train: VigenèreCipher) -> None:
    encoded = vigenere_train.encode("ENCODED IN PYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


@pytest.mark.xfail(reason="Fails with version 1 of VigenèreCipher")
def test_encode_lowercase(vigenere_train: VigenèreCipher) -> None:
    encoded = vigenere_train.encode("encoded in Python")
    assert encoded == "XECWQXUIVCRKHWA"


def test_combine_character() -> None:
    assert combine_character("E", "T") == "X"
    assert combine_character("N", "R") == "E"


def test_extend_keyword(vigenere_train: VigenèreCipher) -> None:
    extended = vigenere_train.extend_keyword(16)
    assert extended == "TRAINTRAINTRAINT"
    extended = vigenere_train.extend_keyword(15)
    assert extended == "TRAINTRAINTRAIN"


# Version 2. Complete.


def test_separate_character() -> None:
    assert separate_character("X", "T") == "E"
    assert separate_character("E", "R") == "N"


from string import ascii_uppercase


def test_combine_separate() -> None:
    for c in ascii_uppercase:
        for k in ascii_uppercase:
            assert separate_character(combine_character(c, k), k) == c


@pytest.fixture
def vigenere_2_train() -> VigenèreCipher_2:
    cipher = VigenèreCipher_2("TRAIN")
    return cipher


def test_encode_2(vigenere_2_train: VigenèreCipher_2) -> None:
    encoded = vigenere_2_train.encode("ENCODEDINPYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


def test_decode_2(vigenere_2_train: VigenèreCipher_2) -> None:
    decoded = vigenere_2_train.decode("XECWQXUIVCRKHWA")
    assert decoded == "ENCODEDINPYTHON"


def test_encode_2_character(vigenere_2_train: VigenèreCipher_2) -> None:
    encoded = vigenere_2_train.encode("E")
    assert encoded == "X"


@pytest.mark.xfail(reason="Fails with version 1 and 2 of VigenèreCipher")
def test_encode_2_spaces(vigenere_2_train: VigenèreCipher_2) -> None:
    encoded = vigenere_2_train.encode("ENCODED IN PYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


@pytest.mark.xfail(reason="Fails with version 1 and 2 of VigenèreCipher")
def test_encode_2_lowercase(vigenere_2_train: VigenèreCipher_2) -> None:
    encoded = vigenere_2_train.encode("encoded in Python")
    assert encoded == "XECWQXUIVCRKHWA"


# Version 3. Optimized.


@pytest.fixture
def vigenere_3_train() -> VigenèreCipher_3:
    cipher = VigenèreCipher_3("TRAIN")
    return cipher


def test_encode_3(vigenere_3_train: VigenèreCipher_3) -> None:
    encoded = vigenere_3_train.encode("ENCODEDINPYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


def test_decode_3(vigenere_3_train: VigenèreCipher_3) -> None:
    decoded = vigenere_3_train.decode("XECWQXUIVCRKHWA")
    assert decoded == "ENCODEDINPYTHON"


def test_encode_3_character(vigenere_3_train: VigenèreCipher_3) -> None:
    encoded = vigenere_3_train.encode("E")
    assert encoded == "X"


def test_encode_3_spaces(vigenere_3_train: VigenèreCipher_3) -> None:
    encoded = vigenere_3_train.encode("ENCODED IN PYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


def test_encode_3_lowercase(vigenere_3_train: VigenèreCipher_3) -> None:
    encoded = vigenere_3_train.encode("encoded in Python")
    assert encoded == "XECWQXUIVCRKHWA"
