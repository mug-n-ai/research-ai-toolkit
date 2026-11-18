"""Regenerate a synthetic calibration figure and its source values.

Run 'python plot.py --seed 7 --output rerun' from this directory with
Matplotlib installed. The bundled CSV gives temperatures in degrees Celsius
and ideal voltages in mV. Add independent uniform offsets between -0.15 and
+0.15 mV to illustrate how a simulation seed affects a result. This toy
perturbation assumes the same spread at all temperatures.

Write 'values.csv' and 'figure.svg' to a new directory. The command reports
invalid arguments, unreadable input or an existing output directory as errors.
"""

import argparse
import csv
from pathlib import Path
import random

from matplotlib import rc_context
from matplotlib.figure import Figure


def main():
    """Read the CLI seed and output directory and write both outputs.

    For example, '--seed 7 --output rerun' creates the two files in 'rerun'.
    Invalid CLI arguments exit with usage help. CSV and filesystem errors
    propagate with the path or value that caused the failure.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    generator = random.Random(args.seed)
    with Path(__file__).with_name("inputs.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    temperatures = [int(row["temperature_c"]) for row in rows]

    # Simulate a bounded voltage perturbation about each ideal calibration value.
    voltages = [
        round(float(row["ideal_voltage_mv"]) + generator.uniform(-0.15, 0.15), 3)
        for row in rows
    ]
    args.output.mkdir(parents=True)
    with (args.output / "values.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["temperature_c", "voltage_mv"])
        writer.writerows(zip(temperatures, (f"{voltage:.3f}" for voltage in voltages)))

    with rc_context({"svg.fonttype": "none", "svg.hashsalt": "calibration-example"}):
        figure = Figure(figsize=(5, 2.9), layout="constrained")
        axis = figure.subplots()
        axis.plot(temperatures, voltages, marker="o", color="#236780")
        axis.set(xlabel="Temperature (°C)", ylabel="Voltage (mV)", ylim=(7.8, 8.8))
        axis.set_xticks(temperatures)
        axis.grid(axis="y", alpha=0.25)
        figure.savefig(args.output / "figure.svg", metadata={"Date": None})


if __name__ == "__main__":
    main()
