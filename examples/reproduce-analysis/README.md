# Rerun a calibration figure with an unknown seed

Use this example to try the [reproduce-analysis skill](../../skills/reproduce-analysis/SKILL.md). The reference run used a synthetic voltage calibration with a random perturbation for each temperature. The run record is missing its seed.

## Input

Share [the reference figure](reference/figure.svg), [its plotted values](reference/values.csv), [the inputs](inputs.csv) and [the plotting script](plot.py). The script and inputs here are the versions used for the reference. The reference used Python 3.12.14 and Matplotlib 3.10.8. Its run record lists the command as `python plot.py --seed <unrecorded> --output reference`.

![Reference calibration figure showing simulated voltage in mV at four temperatures.](reference/figure.svg)

> Use reproduce-analysis to rerun this figure. Keep the reference files and write new outputs elsewhere. If the reference seed is missing, run the supplied workflow with seed 7 to check that the code runs, then tell me what can be reproduced. Compare the voltages at the same temperatures using a tolerance of 0.01 mV per point, and check the axis labels and units.

## Run it

From this directory, in a Python 3.12 environment with Matplotlib 3.10.8, run:

```sh
python plot.py --seed 7 --output rerun
```

This writes `rerun/figure.svg` and `rerun/values.csv`. Choose a fresh output directory if `rerun` already exists.

## Example output

**Status.** Partly reproduced. The supplied code and input produced a figure with the same four temperatures, axis labels and units. All four rerun voltages fell outside the agreed tolerance of 0.01 mV.

| Temperature (°C) | Reference (mV) | Rerun with seed 7 (mV) | Absolute difference (mV) |
| ---: | ---: | ---: | ---: |
| 15 | 8.007 | 7.947 | 0.060 |
| 20 | 8.292 | 8.095 | 0.197 |
| 25 | 8.538 | 8.445 | 0.093 |
| 30 | 8.537 | 8.472 | 0.065 |

**What remains open.** The largest difference is 0.197 mV at 20 °C. Seed 7 was a substitute for the test run. Recover the original seed or the saved perturbation values before checking whether the reference voltages can be reproduced to 0.01 mV.
