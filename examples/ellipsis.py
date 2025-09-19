"""
examples.ellipsis
~~~~~~~~~~~~~~~~~~~~~~

Truncate text that is longer then the terminal.
"""

import time

from yaspin import yaspin

LONG_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer venenatis lectus quis tincidunt "
    "venenatis. Proin interdum neque eu lectus finibus malesuada. Nunc vel nisl quis tellus porta euismod. "
    "Aenean dignissim tortor eu sapien gravida efficitur. Aliquam consectetur aliquam ex facilisis "
    "tincidunt. Nunc luctus arcu nec justo gravida efficitur."
)


def main():
    with yaspin(
        text=f"With ellipsis: {LONG_TEXT}",
        ellipsis="...",
    ) as sp:
        time.sleep(2)

        sp.ellipsis = ""
        sp.text = f"Without ellipsis: {LONG_TEXT}"

        time.sleep(2)


if __name__ == "__main__":
    main()
