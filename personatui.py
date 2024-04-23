import asyncio

from persona.tui_chat import Conversation
from persona.tui import ChatApp

async def main() -> None:
    conversation = Conversation()
    while True:
        msg = input("Type your message: ")
        choices = await conversation.send(msg)
        print("Here are your choices:", choices)
        choice_index = input("Pick your choice: ")
        conversation.pick_response(choices[int(choice_index)])

if __name__ == "__main__":
    app = ChatApp()
    app.run()
