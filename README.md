# MIPP Benchmark: Model Ideology & Personality Profile

## Introduction

The MIPP (Model Ideology & Personality Profile) Benchmark is a novel framework designed to evaluate AI models across a comprehensive set of dimensions including ideological positions, personality traits, cultural awareness, conversational authenticity, and meta-cognitive transparency. Unlike traditional capability benchmarks that focus on *what* a model can do, MIPP aims to reveal the *who* behind the model—its inherent biases, personality characteristics, and worldview, while upholding standards for factual accuracy.

This project provides the questions, rubrics, and (eventually) the scoring and visualization tools to conduct MIPP evaluations.

## Repository Structure

*   `/data/`: Contains the core data files for the benchmark.
    *   `questions.json`: The complete set of questions and prompts for all modules.
    *   `rubrics.json`: Detailed scoring rubrics for evaluating model responses.
    *   `axis_mapping.json`: Configuration for mapping question responses to ideological axes.
*   `/tools/`: Contains Python scripts for processing and analyzing benchmark data.
    *   `scorer.py`: (Partially implemented, design ongoing) Script for loading data, prompting for manual scores, and calculating derived scores.
    *   `visualizer.py`: (Design ongoing) Script for generating model profile cards and comparative visualizations.
*   `/docs/`: (Planned) Will contain further detailed documentation.
    *   `METHODOLOGY.md`: A detailed explanation of the MIPP framework and scoring principles.
*   `README.md`: This file.

## Benchmark Modules

MIPP is structured into four core evaluation modules:

*   **Module A: Ideological Mapping:** Assesses the model's stance across political, economic, social, environmental, technological, and international relations spectra.
*   **Module B: Cultural & Religious Literacy:** Evaluates knowledge of world religions, cultural sensitivity, historical interpretation patterns, and understanding of philosophical traditions.
*   **Module C: Personality & Authenticity:** Tests humor generation, creative expression, and conversational naturalness.
*   **Module D: Meta-Cognitive Transparency:** Probes the model's self-awareness, bias acknowledgment, recognition of its limitations, and disclosure of training patterns.

## Scoring Overview

Model responses to the benchmark questions are evaluated manually by human raters using detailed rubrics provided in `data/rubrics.json`. These rubric scores are then processed by `scorer.py` to generate:

*   **Ideological Coordinates:** Placement on Economic, Social, Authority, and Global axes.
*   **Performance Metrics:** Scores for Factual Accuracy, Consistency, Transparency, and Nuance Recognition.
*   **Personality Profile:** Categorization of Humor and Conversation Styles, and scores for Cultural Fluency and Creativity.
*   **Composite Scores:** An Overall MIPP Score and a Bias Transparency Index.

## Current Status

*   **Data Population:** `questions.json` (435 questions) and `rubrics.json` are fully populated based on the "MIPP Benchmark.txt" specification. `axis_mapping.json` has an initial subset of mappings.
*   **Scoring Logic:** Detailed algorithm specifications for ideological coordinates, performance metrics, personality profiles, and composite scores have been developed.
*   **Python Implementation:** The Python implementation of the scoring (`scorer.py`) and visualization (`visualizer.py`) logic is ongoing. Some parts have been deferred or simplified due to technical challenges in the development environment (persistent `SyntaxError` issues when writing Python scripts). The focus has been on robust data structures and clear algorithmic design.

## How to Use (Conceptual Future Steps)

1.  **Response Collection:** Obtain responses from the target AI model for the questions in `data/questions.json`.
2.  **Manual Evaluation:** Use the `data/rubrics.json` to manually score each response. The `tools/scorer.py` script provides a helper function (`prompt_for_manual_scores`) to facilitate this.
3.  **Score Calculation:** Utilize `tools/scorer.py` (once fully implemented) to process the manual scores and generate the full suite of MIPP metrics and profiles.
4.  **Visualization:** Employ `tools/visualizer.py` (once fully implemented) to generate Model Profile Cards and comparative charts.

## Contributing

Contributions to the MIPP Benchmark are welcome! Please refer to `CONTRIBUTING.md` (to be created) for guidelines.

## License

(To be determined - e.g., MIT License or Apache 2.0. A `LICENSE` file will be added accordingly.)
