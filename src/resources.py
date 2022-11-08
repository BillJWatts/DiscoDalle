import random

CONFIRMATION_MESSAGES = [
    "Getting right on that {artist}!",
    "Great suggestion {artist}",
    "{artist}... wow...",
    "I like how you think {artist}",
    "Ok {artist}, brb",
    "{artist} thinks they're being clever",
    "Give me a sec {artist}",
    "Alright {artist}, on it!",
    "I'm on it {artist}",
    "It's my top priority {artist}!",
    "{artist}, give me a break! ... fine...",
    "I love your imagination {artist}",
    "{artist}! How do even think that up!?",
]


def get_confirmation_message(artist: str) -> str:
    return random.choice(CONFIRMATION_MESSAGES).format(artist=artist)
