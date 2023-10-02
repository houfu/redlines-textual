import click
from redlines import Redlines
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, TextArea, Label, Static


class FormScreen(Screen[Redlines]):
    def __init__(self, source: str = "", test: str = ""):
        super().__init__()
        self.source_textarea = TextArea(source, theme="dracula", id="source")
        self.source_textarea.show_line_numbers = False
        self.test_textarea = TextArea(test, theme="dracula", id="test")
        self.test_textarea.show_line_numbers = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            with Vertical():
                yield Label("Source", classes="form_label")
                yield self.source_textarea
        with Horizontal():
            with Vertical():
                yield Label("Test", classes="form_label")
                yield self.test_textarea
        with Horizontal(classes="action_bar"):
            yield Button(
                "Compare", id="start", variant="primary", classes="form_button"
            )
            yield Button("Reset", id="reset", variant="warning", classes="form_button")
            yield Button("Quit App", id="quit", classes="form_button")

    def action_toggle_dark(self, dark: bool) -> None:
        """An action to toggle dark mode."""
        self.source_textarea.theme = "monokai" if dark else "dracula"
        self.test_textarea.theme = "monokai" if dark else "dracula"

    def on_mount(self):
        self.app.sub_title = "Enter a test and source text to compare"

    @on(Button.Pressed, "#quit")
    def quit(self):
        self.app.exit(message="Thanks for using Redlines!")

    @on(Button.Pressed, "#reset")
    def reset(self):
        """
        Resets the text areas
        """
        self.source_textarea.clear()
        self.test_textarea.clear()

    @on(Button.Pressed, "#start")
    def submit(self):
        """
        Submits the text areas
        """
        # TODO: Validation
        if not self.source_textarea.text or not self.test_textarea.text:
            self.app.sub_title = (
                "ERROR: You need to enter text for both test and source."
            )
            return
        self.app.sub_title = "Comparing..."
        self.app.push_screen(
            ResultsScreen(Redlines(self.source_textarea.text, self.test_textarea.text))
        )


class DocumentViewer(VerticalScroll):
    """
    Displays the document
    """

    def __init__(self, content, border_title="Redline"):
        super().__init__(Static(content, classes="content"), classes="area")
        self.border_title = border_title


class ResultsScreen(Screen):
    """
    Displays the results of the comparison
    """

    def __init__(self, redline: Redlines):
        super().__init__()
        self.redline = redline

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            with Vertical(id="results"):
                yield DocumentViewer(self.redline.output_rich)
            with Vertical():
                yield DocumentViewer(self.redline.source, "Original")
                yield DocumentViewer(self.redline.test, "Test")
        with Horizontal(classes="action_bar"):
            yield Button("Back", id="return", variant="primary", classes="form_button")
            yield Button("Quit App", id="quit", classes="form_button")

    def on_mount(self):
        self.app.sub_title = "Results Screen"

    @on(Button.Pressed, "#quit")
    def quit(self):
        self.app.exit(message="Thanks for using Redlines!")

    @on(Button.Pressed, "#return")
    def return_to_main(self):
        self.app.pop_screen()


class RedlinesApp(App):
    """A textual app to show differences in text"""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("escape", "quit", "Quit App"),
    ]
    CSS_PATH = "app.tcss"
    TITLE = "Redlines App"
    SCREENS = {"form": FormScreen}

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        if isinstance(self.screen, FormScreen):
            self.screen.action_toggle_dark(self.dark)
        self.dark = not self.dark

    def on_mount(self):
        self.push_screen(FormScreen(self.source, self.test))

    def __init__(self, source: str, test: str):
        super().__init__()
        self.source = source
        self.test = test


@click.command()
@click.argument("source", default="")
@click.option("--test", default="", help="Optional test string to fill form")
def run(source: str, test: str):
    """Run the app."""
    app = RedlinesApp(source, test)
    app.run()


if __name__ == "__main__":
    run()
