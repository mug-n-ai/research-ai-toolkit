# Bundled local CLIs

## Bundled local CLIs

Run the examples from this skill directory.

All helpers run offline, reject URLs and symlinks, bound their inputs, write output
atomically with private permissions, and refuse to overwrite without `--force`.

```bash
python scripts/propagate_uncertainty.py --help
python scripts/uncertainty_budget.py --help
python scripts/format_result.py --help
python scripts/convert_units.py --help
python scripts/audit_units.py --help
python scripts/check_plausibility.py --help
```

### propagate_uncertainty.py

Runs both propagation methods on the same numerical model and compares interval
endpoints. This fixed-trial diagnostic does **not** implement the adaptive stabilization
in JCGM 101 7.9/8.2 and never labels the GUM result fully validated.

```bash
python scripts/propagate_uncertainty.py \
  --expression "m / (pi * (d / 2) ** 2 * h)" \
  --variable "m=250.0,0.05" \
  --variable "d=2.0,0.002,rectangular" \
  --variable "h=4.0,0.005,rectangular" \
  --measurand density --unit "g/cm3" --format markdown
```

Each `--variable` is `name=value,standard_uncertainty[,distribution[,dof]]`, where the
distribution is `normal`, `rectangular`, `triangular`, `arcsine`, or `exact` and controls
Monte Carlo sampling only. Here mass is in g and lengths in cm: `--unit` is
a report label, **not** dimensional validation or conversion. JSON variable units are
also labels; convert inputs to a consistent numerical model first. Correlations go in as `--correlation "a,b=0.9"`. A JSON
`--spec` file holds the same model for anything long-lived.
The joint normal sampler supports positive semidefinite correlation matrices, including
perfect correlations. Other joint distributions need a separate sampler. Correlated
finite-dof inputs are refused because independent-input Welch-Satterthwaite is invalid.
For independent finite-dof inputs the CLI's MC PDFs remain fixed: `dof` affects the
GUM factor only, not MC sampling. A small-sample t input needs a separate justified model.

The expression is parsed into an abstract syntax tree and reduced by an explicit walk
over `+ - * / **` and a fixed list of functions. It is never compiled or executed.

The report gives the estimate, `u_c`, sensitivity coefficients, the budget in percent,
effective degrees of freedom, `k`, `U`, both Monte Carlo coverage intervals, and the
endpoint-agreement diagnostic. Repeat/increase sampling and verify model/PDF
assumptions before deciding what to report.

### uncertainty_budget.py

Combines components stated the way certificates and data sheets state them.

```bash
python scripts/uncertainty_budget.py --template > budget.json
python scripts/uncertainty_budget.py --spec budget.json --format markdown
```

Each component names a `distribution` that fixes its divisor — `expanded` divides by its
`coverage_factor`, `rectangular` by `sqrt(3)`, `triangular` by `sqrt(6)`, `arcsine` by
`sqrt(2)`, `normal` by 1 — with an optional `sensitivity`, `dof`, and `relative: true`.
The tool assumes independent components, requires an explicit factor for `expanded`,
and rejects nonzero `exact` components. It computes `u_c`, effective degrees of freedom, `k` from
the t-distribution, and `U`, and warns when a Type A component has no degrees of
freedom, when `nu_eff` is small enough that `k = 2` is wrong, when one component
dominates, and when a Type B component declared `normal` is probably an undivided
expanded uncertainty.

### format_result.py

```bash
python scripts/format_result.py \
  --value 12.34567 --uncertainty 0.02345 --unit mm \
  --coverage-factor 2.26 --coverage-probability 0.95
```

Returns `12.346 ± 0.023 mm`, `12.346(23) mm`, the scientific and LaTeX forms, and the
sentence that has to accompany the number. Warns when one significant digit is requested
for an uncertainty beginning in 1 or 2, and when the uncertainty exceeds the estimate.

### convert_units.py

```bash
python scripts/convert_units.py \
  --value 532 --unit nm --to eV --context spectroscopy --uncertainty 0.5

python scripts/convert_units.py \
  --value 1.0 --unit g --to mol --context chemistry --context-parameter "mw=180.156 g/mol"
```

Carries the uncertainty through the conversion's local derivative. Some contexts
(such as wavelength to energy) are reciprocal, whereas others are proportional.
Context parameters (`mw`, `n`) are treated as exact; their uncertainties need an
explicit measurement model. Offset-temperature uncertainty units are differences. Names the context in the
error message when a conversion needs one, and flags offset and logarithmic units.
`--list-contexts` shows what the registry defines.

### audit_units.py

Static review of existing analysis code. Parses, never imports or runs.

```bash
python scripts/audit_units.py \
  --input analysis.py --format markdown --fail-on medium
```

| Rule | Severity | Detects |
| --- | --- | --- |
| `UNIT001` | medium | a second `UnitRegistry` in one module — cross-registry `ValueError` |
| `UNIT002` | medium | offset temperature units with no `delta_` unit anywhere |
| `UNIT003` | high | `.magnitude` without a preceding `.to(...)` or `.m_as(...)` |
| `UNIT004` | medium | logarithmic units, whose `+` multiplies |
| `UNC001` | high | `curve_fit` without `absolute_sigma` |
| `UNC002` | medium | `np.std` / `np.var` without `ddof` or NumPy's `correction` alias |
| `UNC003` | medium | `math` or `numpy` functions in a module that uses `uncertainties` |
| `UNC004` | high | a `ufloat` rebuilt from `.nominal_value` and `.std_dev` |
| `CONST001` | low | a literal within 0.1% of a CODATA constant |

Exit status is 1 when a finding meets `--fail-on` (default `high`), which makes it usable
as a pre-commit or CI check.

The rules are heuristics, so a false positive is suppressed with a directive comment —
trailing to cover its own line, or alone on a line to cover the next one:

```python
value = quantity.magnitude  # audit-units: ignore UNIT003 -- already converted upstream

# audit-units: ignore UNC003 -- the argument here is a plain float array
scaled = np.log10(counts)
```

`# audit-units: ignore-file CONST001` covers a whole module, and naming no rule
suppresses all of them. Suppressions are counted in the report rather than hidden, so a
file that silences everything still says so.

### check_plausibility.py

Dimensional consistency is not physical possibility. A cell 2 m across and a Reynolds
number of 4e7 in a capillary both pass every unit check. This tool tests a set of
quantities against dimensionless groups, characteristic scales, and illustrative typical-value
bands, and verifies each formula's dimensionality before reporting a number.

```bash
python scripts/check_plausibility.py \
  --quantity "density=1060 kg/m**3" --quantity "velocity=0.5 mm/s" \
  --quantity "length=8 um" --quantity "viscosity=3.5 mPa*s" \
  --group reynolds --format markdown
# Re = 0.001211 -- laminar (circular pipe, length = diameter)

python scripts/check_plausibility.py \
  --quantity "diameter=2 m" --band "eukaryotic_cell_diameter=diameter"
# implausible: 4.3 decades outside the 5-100 um range
```

`--group` evaluates one of 14 dimensionless groups and names the regime it places the
system in; `--scale` computes a characteristic scale such as a diffusion time, Debye
length, or Stokes settling velocity; `--band` compares a supplied quantity against an
observed range. `--list` prints the whole catalogue with the inputs each formula needs.

Physical constants (`k_B`, `N_A`, `R_gas`, `g_earth`, and the rest) are available to every
formula without being supplied. Their nominal values come from `scipy.constants`;
this plausibility helper does not propagate their uncertainties. `g_earth` is standard
gravity, not a local measurement. Bands are screening heuristics, not physical limits.

The dimensionality check is the point. Passing a kinematic viscosity where the formula
needs a dynamic one — both called "viscosity", both tabulated for water, differing by a
factor of ρ — is refused before any number is computed:

```
error: viscosity must have dimensionality [mass] / ([length] * [time]),
       but m²/s is [length] ** 2 / [time]
```

Exit status is 1 when the verdict meets `--fail-on` (default `implausible`; a value
within one decade of a band is `questionable`). The thresholds are conventions with soft
edges and assume the geometry their correlation was fitted for — see
`references/plausibility-scales.md` for the characteristic length to use in each case.
