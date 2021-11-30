# pylint: disable=W0613,W0107,W0611,C0200
"""This module is the implementation of hangman.py"""
import random
import re
import message
from error import InputError, AccessError
from database import database
from hangman_states import HANGMAN_STATE

def generate_word():
    '''generates a random word'''
    filename = "/usr/share/dict/british-english"
    candidates = [x.strip().lower() for x in open(filename, "r")]
    word = candidates[(random.randint(0, len(candidates) - 1))]
    return word

def hangman_start(channel_id):
    '''Starts a game of hangman'''
    channel = database.get_channel_by_id(channel_id)
    hangman_info = channel.start_hangman(generate_word())
    word = " ".join(hangman_info['word_guess'])
    hangman_state = (
        "\nWelcome to Hangman!\n"
        """Use '/guess (letter)' to guess letter
        """
        f"\nWord: {word}"
        )
    return hangman_state

def hangman_guess(channel_id, char):
    '''Guess a letter in hangman'''
    if not re.match("^[a-zA-Z']$", char):
        raise InputError("Incorrect Input")
    channel = database.get_channel_by_id(channel_id)
    hangman_info = channel.get_hangman_state()
    if hangman_info["state_count"] == -1:
        return "No hangman game running. Use /hangman to start."
    if char in hangman_info['guessed_letters'] or char in hangman_info['word_guess']:
        return "Letter already guessed"
    for i in range(len(hangman_info['word'])):
        if char == hangman_info['word'][i]:
            channel.fill_hangman_letter(char, i)
    if char not in hangman_info['word']:
        channel.increment_hangman_state_count()
        channel.add_hangman_letter(char)
    hangman_info = channel.get_hangman_state()
    state_count = hangman_info["state_count"]
    word = " ".join(hangman_info['word_guess'])
    guessed_letters = ", ".join(hangman_info['guessed_letters'])

    hangman_state = (
        f"Hangman:\n{HANGMAN_STATE[state_count]}"
        f"\n\nWord: {word}\n"
        f"Letters Guessed: {guessed_letters}"
        )

    if "_" not in hangman_info['word_guess']:
        channel.hangman_end()
        return hangman_state + "\nCongrats!"

    if hangman_info["state_count"] == 10:
        channel.hangman_end()
        return hangman_state + f"\nYou suck!\nThe word was {hangman_info['word']}"
    return hangman_state
