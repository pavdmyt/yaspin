# -*- coding: utf-8 -*-

import time
import yaspin


# Refer here for more spinner examples
# https://github.com/sindresorhus/cli-spinners
def main():
    params = [
        ("Braille",  "",            None),
        ("Line",     "-\\|/",       0.15),
        ("Flip",    "___-``'´-___", 0.07),
        ("Dot",     "⠁⠂⠄⠂",        0.12),
        ("Dots",    u"⢄⢂⢁⡁⡈⡐⡠",    0.08),
        ("Balloon",  ".oOo. ",      0.14),
        ("Star",     "+x*",         0.08),
    ]
    for p in params:
        with yaspin.spinner(*p):
            time.sleep(3)


if __name__ == '__main__':
    main()
