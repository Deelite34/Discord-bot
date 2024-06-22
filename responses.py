from random import choice


responses = {
    "": "Well, you're awfully silent...",
    "hello": "Hello there!",
    "bye": "See you!",
    "help": "You can prepend command with '?' if you want to received response as direct message. "
    "Available commands: hello, bye, help",
}


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    return responses.get(
        lowered, choice(["I do not understand.", "I do not know this phrase."])
    )
