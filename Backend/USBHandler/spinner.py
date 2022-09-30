################################################################################


# Based on a StackOverflow thread :
# https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running


################################################################################


from threading import Thread
from time import sleep
from itertools import cycle


################################################################################


class spinner:
    def __init__(self, desc='Processing...', end='Done', timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["[⢿]", "[⣻]", "[⣽]", "[⣾]", "[⣷]", "[⣯]", "[⣟]", "[⡿]"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{c}  {self.desc}", flush=True, end="\r")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        print(' '*(len(self.desc) + 5), end="\r")
        self.done = True

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()


################################################################################


if __name__ == "__main__":
    with spinner("Spinning demo..."):
        for i in range(10):
            sleep(0.25)