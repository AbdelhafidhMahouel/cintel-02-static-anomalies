# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
The dataset used in this project comes from a pediatric clinic and includes patient records with two fields: age in years and height in inches. Each row represents one patient visit. I created my own version of the dataset named `clinic_data_abdel.csv` to test my custom anomaly detection logic.

### Signals
The main signals used in this project are:
- age_years
- height_inches

I also created a new signal called `anomaly_reason`, which explains why a data point is considered an anomaly. This helps make the results easier to understand.

### Experiments
For my experiment, I modified the anomaly detection thresholds:
- I changed the maximum age from 16 to 15
- I changed the maximum height from 72 inches to 70 inches
- I added minimum thresholds (age cannot be below 0 and height cannot be below 20 inches)

I also updated the logic to detect both high and low anomalies instead of only high values.

### Results
After running the modified pipeline, the system successfully detected anomalies and saved them in `artifacts/anomalies_abdel.csv`. Compared to the original example, more anomalies were detected because the thresholds were stricter and included both upper and lower limits.

### Interpretation
These results show that changing thresholds can significantly affect anomaly detection. By adding lower limits and explanation labels, the system becomes more informative and useful. This can help analysts quickly identify unusual data and understand why it was flagged, which improves decision-making in real-world systems.
