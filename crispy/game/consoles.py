class Console:

    def __init__(self, text=None):
        if text is None:
            text = ""
        self.text = "\n"
        self.add(text)

    def get(self):
        return self.text

    def add(self, maybe_text):
        try:
            self.text += " " + maybe_text + "\n"
        except TypeError:
            self.text += " " + str(maybe_text) + "\n"

    def clear(self):
        self.text = "\n"
        self.add("Console cleared.")
