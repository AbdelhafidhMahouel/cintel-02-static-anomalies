# cintel-02-static-anomalies

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](#)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project for continuous intelligence.

Continuous intelligence systems monitor data streams, detect change, and respond in real time.
This course builds those capabilities through working projects.

In the age of generative AI, durable skills are grounded in real work:
setting up a professional environment,
reading and running code,
understanding the logic,
and pushing work to a shared repository.
Each project follows the structure of professional Python projects.
We learn by doing.

---

## This Project

This project introduces **static anomaly detection**.

The goal is to copy this repository,
set up your environment,
run the example analysis,
and explore how anomalies are identified in static data.

You will run the example pipeline, read the code,
and make small modifications to understand how
the detection logic works.

---

## Data

The example pipeline reads **pediatric clinic** age and height
data from:

data/clinic_data_case.csv

It creates reasonable thresholds and outputs
**anomalies** (data outside the expected threshold).

For my custom version I created:

data/clinic_data_abdel.csv

The anomaly results are saved to:

artifacts/anomalies_abdel.csv

---

## Working Files

You'll work with just these areas:

- **data/** – input datasets
- **docs/** – documentation
- **src/cintel/** – where the pipeline code runs
- **pyproject.toml** – project configuration
- **zensical.toml** – documentation configuration

---

## Instructions

Follow the workflow guide:

https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/

Complete the phases:

1. Phase 1 – Start & Run
2. Phase 2 – Change Authorship
3. Phase 3 – Read & Understand
4. Phase 4 – Make a Technical Modification
5. Phase 5 – Apply the Skills to a New Problem

---

## Phase 4 – Technical Modification

For Phase 4 I created a new pipeline script:

src/cintel/anomaly_detector_abdel.py

### What I Changed

I made several modifications to the anomaly detection logic:

- Changed the anomaly thresholds
  - maximum age changed from **16** to **15**
  - maximum height changed from **72 inches** to **70 inches**

- Added lower bound validation
  - age cannot be negative
  - height cannot be less than **20 inches**

- Added a new column called **anomaly_reason**
  explaining why each record was flagged

Example reasons:

- age too high
- height too high
- age too low
- height too low

- Sorted the anomaly output to make it easier to read.

### Why I Made These Changes

I wanted the anomaly detection to be more complete and easier to interpret.
The original example only detected values that were too high.
My version also detects values that are too low and explains the reason for each anomaly.

### What I Observed

After running the modified script, the pipeline executed successfully
and produced a new anomalies file in the artifacts folder.

Because the thresholds are stricter, more records were flagged as anomalies.

### What I Learned

This exercise showed how small changes in thresholds
can significantly change anomaly detection results.

It also showed that adding explanation columns
helps make results easier to interpret.

---

## Challenges

Challenges are expected.
Sometimes instructions may not quite match your operating system.

When issues occur, share:

- screenshots
- error messages
- steps you attempted

Working through issues is part of implementing professional projects.

---

## Success

After running the pipeline successfully the terminal prints:

```shell
========================
Pipeline executed successfully!
========================
```

And a new file named `project.log` will appear in the project folder.

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
git clone https://github.com/AbdelhafidhMahouel/cintel-02-static-anomalies

cd cintel-02-static-anomalies
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
git add -A
uvx pre-commit run --all-files

uv run python -m cintel.anomaly_detector_case
uv run python -m cintel.anomaly_detector_abdel

uv run ruff format .
uv run ruff check . --fix
uv run zensical build

git add -A
git commit -m "add custom anomaly detection modification"
git push -u origin main
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.
