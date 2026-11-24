# Equations and physics in a research report

This is a technical explanation of the researcher's model, not a new derivation presented as an established finding. Begin from the physical question, the observable or simulated quantity, and the regime being studied. Read the underlying implementation, working notes or source before describing the model.

For every governing equation, introduce its purpose, define all symbols and units, identify which parameters are fixed or fitted, and state the assumptions that make it valid. Explain significant transitions in a derivation rather than writing a chain of unexplained equalities. Distinguish exact identities, approximations, numerical schemes, empirical fits, priors and illustrative examples; state the approximation order or valid regime where known.

Perform dimensional, limiting-case and sign-convention checks when appropriate. For physical models, consider conservation laws, boundary and initial conditions and the relationship between model outputs and measured observables. A dimensional match is necessary but does not establish that a result is physically plausible.

When reporting uncertainty, distinguish measurement error, numerical error, sampling variability, model inadequacy and posterior uncertainty. State what reported intervals mean, correlations that matter and any approximation to their propagation. Use `uncertainty-and-units` if installed and relevant; don't manufacture uncertainties missing from the source analysis.

Use numbered and labelled displayed equations only when the reader needs to refer to them. Link each derived result to the calculation, simulation or supporting source. Separate what was verified, what is taken from the supplied notes, and what remains a hypothesis or check to perform.

