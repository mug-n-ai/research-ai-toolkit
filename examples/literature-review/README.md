# Check what a paper supports

Use this example to try the [literature-review skill](../../skills/literature-review/SKILL.md) on one claim. The [full source](source.md) is a fictional lab note with one figure and its data. Share the note and the original figure with the assistant before giving it the task.

## Input

> Apply the literature-review skill to this sentence using the supplied lab note. Check the methods and Figure 1, then suggest wording I could put in a draft. “The correction reduces the mean absolute voltage error by at least 30% across the detector's operating temperature range.”

## Example output

**Evidence.** The note compares four paired measurements at 20 °C. Mean absolute error falls from 5.0 to 3.0 mV, a 40% reduction for those runs. The values come from the table in [Results](source.md#results). The [original Figure 1](paired-errors.svg) shows lower error in each pair.

**Suggested wording.** “In four paired measurements at 20 °C, the correction reduced mean absolute voltage error from 5.0 to 3.0 mV, a decrease of 40%.” Cite the lab note's [Methods and Results](source.md#methods).

**Review record.** The note was read in full and its one figure and caption were inspected. The methods cover one temperature. The 40% is a descriptive result for four pairs. Measurements at other temperatures and an uncertainty analysis would be needed to assess a lower bound across the operating range.

If the assistant can read the text but cannot open the figure, its report should leave visual inspection pending and identify the missing file.
