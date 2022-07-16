"""
examples.hide_show_prompt_toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage of the ``hide`` and ``show`` methods with prompt_toolkit's printing.
Starting from yaspin v1.1.0 handled by ``hidden`` context manager.

Requires python-prompt-tooklit >= 2.0.1
https://github.com/jonathanslenders/python-prompt-toolkit/

.. code:: bash
    pip install "prompt_toolkit>=2.0.1"
"""

import sys
import time

from yaspin import yaspin


try:
    from prompt_toolkit import HTML, print_formatted_text
    from prompt_toolkit.styles import Style
except ImportError:
    print(
        "This example requires python-prompt-tooklit >= 2.0.1:\n"
        "https://github.com/jonathanslenders/python-prompt-toolkit/\n"
        "\nTo install it, run:\n"
        'pip install "prompt_toolkit>=2.0.1"'
    )
    sys.exit(1)


# override print with feature-rich ``print_formatted_text`` from prompt_toolkit
print = print_formatted_text

# build a basic prompt_toolkit style for styling the HTML wrapped text
style = Style.from_dict({"msg": "#4caf50 bold", "sub-msg": "#616161 italic"})


with yaspin(text="Downloading images") as sp:

    # task 1
    time.sleep(1)
    with sp.hidden():
        print(
            HTML("<b>></b> <msg>image 1</msg> <sub-msg>download complete</sub-msg>"),
            style=style,
        )

    # task 2
    time.sleep(2)
    with sp.hidden():
        print(
            HTML("<b>></b> <msg>image 2</msg> <sub-msg>download complete</sub-msg>"),
            style=style,
        )

    # finalize
    sp.green.ok("✔")
