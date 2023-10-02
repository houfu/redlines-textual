from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static


class TestApp(App):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(Static(
                 """
             When the Supreme Court returns to the bench on Monday, it will face a docket filled with unfinished business. The justices will revisit issues like gun rights, government power, race and free speech even as they are shadowed by intense scrutiny of their conduct off the bench.
 
 In the coming months, moreover, the court will very likely agree to hear a major abortion case, one that could severely limit the availability of a drug used in more than half of all pregnancy terminations. A decision in that case could come in June, two years after the court overturned Roe v. Wade.
 
 Recent history suggests that the court’s six Republican appointees will continue to move the law to the right. The main questions are how far, how fast and what impact the questions swirling around the justices’ ethical standards will have on their judicial work and personal relationships.
             """
             ))


def run():
    app = TestApp()
    app.run()


if __name__ == "__main__":
    run()
