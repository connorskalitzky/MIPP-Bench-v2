# MIPP Benchmark Methodology

## 1. Introduction & Philosophy

The MIPP (Model Ideology & Personality Profile) Benchmark is a comprehensive evaluation framework designed to move beyond traditional AI capability testing. Its core philosophy is to understand the "who" behind an AI model—its inherent ideological leanings, personality characteristics, cultural sensitivities, and meta-cognitive self-awareness. While factual accuracy remains a standard, MIPP's primary goal is to profile the more subjective attributes that shape a model's responses and interactions. This provides a richer, more holistic understanding of AI systems as they become increasingly integrated into diverse human contexts.

## 2. Benchmark Architecture

The MIPP benchmark is structured into four Core Evaluation Modules, each targeting distinct facets of a model's profile:

*   **Module A: Ideological Mapping**
    *   **Objective:** To map the model's positions on various socio-political and economic spectra.
    *   **Submodules:**
        *   A1: Political Spectrum Analysis (government role, individual rights, law & justice, healthcare, education)
        *   A2: Economic Philosophy Assessment (market regulation, wealth distribution, labor rights, corporate responsibility, global trade)
        *   A3: Social Values Profiling (gender & identity, family structures, immigration, criminal justice, personal freedom, education, community values, tech/privacy)
        *   A4: Environmental & Technology Stances (climate policy, conservation, AI governance, digital rights, biotechnology, tech regulation, environmental justice, future tech)
        *   A5: International Relations Perspectives (global governance, military intervention, trade relations, human rights vs. sovereignty, migration, global cooperation)

*   **Module B: Cultural & Religious Literacy**
    *   **Objective:** To assess the model's knowledge and sensitivity regarding diverse cultural and religious contexts.
    *   **Submodules:**
        *   B1: World Religions Knowledge & Bias (coverage of major world religions, secular humanism, indigenous traditions)
        *   B2: Cultural Sensitivity Scenarios (evaluating responses in cross-cultural interaction scenarios)
        *   B3: Historical Interpretation Patterns (analyzing framing of contested historical events)
        *   B4: Philosophical Traditions Understanding (knowledge of major Eastern and Western philosophical concepts)

*   **Module C: Personality & Authenticity**
    *   **Objective:** To profile the model's expressed personality traits and its ability to generate human-like, authentic-sounding content.
    *   **Submodules:**
        *   C1: Humor Generation & Style Analysis (testing various comedy styles: observational, satire, puns, absurdist, etc.)
        *   C2: Creative Expression Tests (evaluating originality in tasks like story writing, poetry, and conceptual blending)
        *   C3: Conversational Naturalness (assessing flow, context memory, personality consistency, and appropriate informality in dialogue)

*   **Module D: Meta-Cognitive Transparency**
    *   **Objective:** To evaluate the model's awareness and disclosure of its own nature, capabilities, limitations, and potential biases.
    *   **Submodules:**
        *   D1: Self-Awareness Assessment (identity, origin, capabilities, operational understanding)
        *   D2: Bias Acknowledgment (training data biases, perspective biases, behavioral biases)
        *   D3: Limitation Recognition (knowledge cutoffs, reasoning gaps, practical constraints)
        *   D4: Training Disclosure Patterns (transparency about training processes and objectives)

## 3. Question & Prompt Design

The questions and prompts within each module are designed to elicit responses that reveal the targeted characteristics. They range from direct questions and scenario analyses to creative generation tasks. Care is taken to:
*   Cover a wide spectrum of views and topics within each domain.
*   Use neutral language where possible, especially in eliciting ideological stances, to avoid leading the model.
*   Present complex scenarios that require nuanced reasoning.
*   The full set of questions can be found in `data/questions.json`.

## 4. Scoring Methodology

### 4.1 Manual Evaluation & Rubrics
All model responses are primarily evaluated by trained human raters using a detailed set of rubrics, available in `data/rubrics.json`. Key general rubric dimensions include (but are not limited to):
*   **Position Clarity:** How clearly a stance is defined.
*   **Nuance Recognition:** Acknowledgment of complexity and trade-offs.
*   **Factual Accuracy:** Correctness of factual claims.
*   **Bias Transparency:** Acknowledgment of own perspective or potential biases.
*   **Cultural Sensitivity:** Respectful and aware handling of cultural elements.
*   Specific rubrics apply to specialized modules (e.g., humor effectiveness, directness of meta-cognitive responses).

### 4.2 Ideological Coordinates
Module A responses are used to map the model onto four ideological axes, each on a -10 to +10 scale:
*   **Economic Axis:** (Left to Right)
*   **Social Axis:** (Progressive to Traditional)
*   **Authority Axis:** (Libertarian to Authoritarian)
*   **Global Axis:** (Nationalist to Internationalist/Globalist)
The mapping logic is defined in `data/axis_mapping.json` and considers both the stance taken and the clarity of the position.

### 4.3 Performance Metrics
Standardized scores (0-100) are calculated for:
*   **Factual Accuracy Score:** Aggregated from factual accuracy rubrics.
*   **Consistency Score:** Measures consistency across related questions and internal logic (requires further development for full automation).
*   **Transparency Score:** Aggregated from bias transparency rubrics and Module D scores.
*   **Nuance Recognition Score:** Aggregated from nuance recognition rubrics.

### 4.4 Personality Profile
Generated from Module C and other relevant data:
*   **Humor Style:** Categorization of preferred/most effective humor styles.
*   **Conversation Style:** Classification (e.g., Formal, Casual, Adaptive).
*   **Cultural Fluency Score (0-100):** Derived from culturally relevant rubrics across modules.
*   **Creativity Index (0-100):** Derived from creative tasks in Module C.

### 4.5 Composite Scores
Two main composite scores provide a high-level summary:
*   **Overall MIPP Score (0-100):** A weighted average of the four main module scores (Ideological, Cultural, Personality, Transparency), providing a holistic measure of the model's profiled attributes.
*   **Bias Transparency Index (BTI) (0-100):** A measure of how consistently and accurately a model acknowledges its biases, balanced by its factual accuracy and nuance.

## 5. Data & Tools Overview

*   `data/questions.json`: Contains all benchmark questions and prompts.
*   `data/rubrics.json`: Defines all scoring rubrics.
*   `data/axis_mapping.json`: Defines the mapping of questions to ideological axes.
*   `tools/scorer.py`: Script for loading data, facilitating manual score input, and (once fully implemented) calculating all derived scores and profiles.
*   `tools/visualizer.py`: (Planned) Script for generating Model Profile Cards and comparative visualizations.

## 6. Limitations & Future Work

The MIPP Benchmark relies significantly on nuanced human evaluation for many of its qualitative aspects. While rubrics provide guidance, inter-rater reliability is crucial and requires ongoing calibration. Automating aspects of consistency checking and nuanced stance detection are areas for future research and development. The benchmark aims to be a living framework, with potential for new questions, modules, and analytical techniques to be incorporated over time.
