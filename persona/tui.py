from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Button, Static
from textual.widget import Widget
from textual.containers import Container, Horizontal

class ChatApp(App):
    '''A chat application.'''
    TITLE = "chatui"
    SUB_TITLE = "ChatGPT directly in your terminal"
    CSS_PATH = "static/styles.css"

    def compose(self) -> ComposeResult:
        '''Compose the widgets.'''
        yield Header()
        yield Container(id="conversation_box")
        with Horizontal(id="input_box"):
            yield Input(placeholder="Enter your message", id="message_input")
            yield Button(label="Send", variant="success", id="send_button")
        yield Footer()


    async def on_button_pressed(self) -> None:
        '''Handle the button press.'''
        await self.process_conversation()

    async def on_input_submitted(self) -> None:
        '''Handle the input submission.'''
        await self.process_conversation()

    async def process_conversation(self) -> None:
        '''Process the conversation.'''
        message_input = self.query_one("#message_input", Input)
        # Don't do anything if input is empty
        if message_input.value == "":
            return
        button = self.query_one("#send_button")
        conversation_box = self.query_one("#conversation_box")  # 🆕

        self.toggle_widgets(message_input, button)

        # 🆕 Create question message, add it to the conversation and scroll down
        message_box = MessageBox(message_input.value, "question")
        conversation_box.mount(message_box)
        conversation_box.scroll_end(duration=0.5, animate=True)

        # Clean up the input without triggering events
        with message_input.prevent(Input.Changed):
            message_input.value = ""

        # 🆕 Add answer to the conversation
        conversation_box.mount(
            MessageBox(
                "Answer",
                "answer",
            )
        )
        self.toggle_widgets(message_input, button)
        conversation_box.scroll_end(duration=0.5, animate=True) 

    def toggle_widgets(self, *widgets: Widget) -> None:
        '''Toggle the disabled state of the widgets.'''
        for w in widgets:
            w.disabled = not w.disabled

class MessageBox(Widget):
    '''A message box that displays a message with a role.'''
    def __init__(self, text: str, role: str) -> None:
        '''Initialize the message box with text and role.'''
        self.text = text
        self.role = role
        super().__init__()

    def compose(self) -> ComposeResult:
        '''Compose the message box.'''
        yield Static(self.text, classes=f"message {self.role}")

    
     