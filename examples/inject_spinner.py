import signal
import time

from yaspin import inject_spinner
from yaspin.core import default_handler, Yaspin
from yaspin.spinners import Spinners

SLEEP = 2


# Basic usage
@inject_spinner()
def simple_task(spinner: Yaspin, items: list) -> None:
    for i, _ in enumerate(items, 1):
        spinner.text = f"Processing item {i}/{len(items)}"
        time.sleep(SLEEP)
    spinner.ok("✓")


# With spinner customization
@inject_spinner(Spinners.dots, text="Processing...", color="green")
def process_items(spinner: Yaspin, items: list) -> None:
    for i, _ in enumerate(items, 1):
        spinner.text = f"Processing item {i}/{len(items)}"
        spinner.color = "yellow" if i % 2 == 0 else "cyan"
        time.sleep(SLEEP)
    spinner.ok("✓")


# With signal handling
@inject_spinner(sigmap={signal.SIGINT: default_handler})
def safe_process(spinner: Yaspin, items: list) -> None:
    spinner.text = "Press Ctrl+C to interrupt..."
    time.sleep(5)
    spinner.ok("✓")


def main():
    items = ["item1", "item2", "item3"]
    simple_task(items)
    process_items(items)
    safe_process(items)


if __name__ == "__main__":
    main()
