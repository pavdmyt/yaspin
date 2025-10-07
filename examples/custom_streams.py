"""
Real-world example demonstrating the stream parameter usage.
This simulates the main use case: python script.py > output.log
"""

import json
import sys
import time

from yaspin import yaspin


def simulate_json_processing():
    """Simulate a data processing script that outputs JSON while showing progress"""
    with yaspin(stream=sys.stderr, text="Processing data...") as spinner:
        for i in range(5):
            data = {"id": i, "value": f"data_{i}", "processed": True}
            print(json.dumps(data))  # This goes to stdout
            time.sleep(0.3)
        spinner.ok("✓ Processing complete")


if __name__ == "__main__":
    simulate_json_processing()

    print("\nTo test redirection, run:")
    print("  python custom_streams.py > output.log")
    print("  cat output.log  # Should contain only JSON data")
