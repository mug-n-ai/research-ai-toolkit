"""Replot the four datasets from Anscombe (1973), section 3.

Run 'python plot.py --output rerun' with Matplotlib installed. The input is
the adjacent anscombe.csv, transcribed from the paper. Each dataset contains
unitless x and y values. The script fits y = intercept + slope * x by
ordinary least squares, with an intercept, and reports squared Pearson
correlation as R². It computes no inference about whether a line is a good
model for the data.

The command creates figure.svg and fits.csv in a new output directory.
Malformed inputs, constant predictors and an existing directory raise errors.
"""

import argparse
import csv
from pathlib import Path
from statistics import correlation, linear_regression

from matplotlib import rc_context
from matplotlib.figure import Figure


def main():
    """Fit and plot all four columns and write the figure and fit table.

    For example, '--output rerun' writes both files to 'rerun' without
    overwriting a prior run. Invalid CLI arguments exit with usage help.
    CSV conversion, regression and filesystem errors propagate to the caller.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = Path(__file__).with_name("anscombe.csv")
    with source.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    args.output.mkdir(parents=True)
    with rc_context({"svg.fonttype": "none", "svg.hashsalt": "anscombe-reproduction"}):
        figure = Figure(figsize=(7.6, 5.6), layout="constrained")
        axes = figure.subplots(2, 2, sharex=True, sharey=True)
        figure.supxlabel("x")
        figure.supylabel("y")
        with (args.output / "fits.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(["dataset", "n", "intercept", "slope", "r_squared"])
            for number, (label, axis) in enumerate(zip(("I", "II", "III", "IV"), axes.flat), 1):
                x_column = "x4" if number == 4 else "x123"
                x = [float(row[x_column]) for row in rows]
                y = [float(row[f"y{number}"]) for row in rows]
                slope, intercept = linear_regression(x, y)
                r_squared = correlation(x, y) ** 2
                writer.writerow([
                    label, len(x), f"{intercept:.6f}", f"{slope:.6f}", f"{r_squared:.6f}",
                ])

                axis.plot((0, 20), (intercept, intercept + 20 * slope), color="#8a4d25")
                axis.scatter(x, y, s=21, color="#236780", zorder=3)
                axis.set(
                    title=f"Set {label}", xlim=(0, 20), ylim=(0, 14),
                    xticks=(0, 5, 10, 15, 20), yticks=(0, 5, 10),
                )
                axis.grid(alpha=0.22)
        figure.savefig(args.output / "figure.svg", metadata={"Date": None})


if __name__ == "__main__":
    main()
