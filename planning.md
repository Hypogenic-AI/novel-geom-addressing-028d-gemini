# Research Plan: Addressability of Repeated Novel Geometries

## Research Question
Can novel 2D geometries, learned in-context from coordinate data, be reliably addressed using verbal labels? What is the minimum repetition required for this mapping to become stable, and does it enable reasoning about spatial relationships without explicit instruction?

## Motivation & Novelty Assessment

### Why This Research Matters
LLMs are being integrated into workflows requiring spatial understanding (e.g., UI automation, robotics, design). The ability to "name" and subsequently "address" novel spatial configurations in a few-shot manner is a key capability for these applications.

### Gap in Existing Work
While papers like arXiv:2501.00070 show that models can learn the *topology* of a hidden graph in-context, they don't focus on the *semantic addressing* of specific nodes in a 2D geometric context. Most spatial reasoning benchmarks are either zero-shot or require extensive few-shot examples. We focus on the *minimalist* regime (1-5 repetitions).

### Our Novel Contribution
We explicitly test the "addressability" threshold: the point where a model stops treating a coordinate string as an opaque token and starts treating it as a named entity with spatial properties.

### Experiment Justification
- **Experiment 1: The Addressability Threshold.** We will use the KiloGram dataset (SVGs of tangrams) to define novel geometries. We will vary the number of examples (shots) and test the model's ability to return the coordinates of a named part.
- **Experiment 2: Zero-shot Spatial Reasoning.** Once a geometry is "addressed" (named), we test if the model can answer spatial queries (e.g., "Is part A to the left of part B?") that were not explicitly stated, testing if a geometric representation has been formed.

## Hypothesis Decomposition
1. **H1 (Threshold):** There is a sharp phase transition (as suggested by 2501.00070) in addressability, likely around 3-5 repetitions.
2. **H2 (Reasoning):** Models can perform simple spatial reasoning (above/below/left/right) on addressed parts even if the relative positions were never explicitly mentioned in the context, provided the coordinates were given.

## Proposed Methodology

### Approach
We will use text-only prompts containing SVG-like coordinate strings for novel shapes from the KiloGram dataset. Each shape consists of multiple parts with names.

### Experimental Steps
1. **Data Selection:** Select 10-20 distinct tangram shapes from `code/kilogram/dataset/tangrams-svg/`.
2. **Prompt Engineering:**
   - Define a "Geometry Definition" format: `[Name]: [Coordinates]`.
   - Create few-shot sequences with $N$ repetitions ($N \in \{1, 2, 3, 5, 10\}$).
3. **Task 1 (Addressing):** "Given the geometry defined above, what are the coordinates of the [Part Name]?"
4. **Task 2 (Spatial Reasoning):** "In the geometry defined above, is the [Part A] above the [Part B]?"
5. **Baseline:** Zero-shot performance (model guessing or using general knowledge of tangrams).

### Baselines
- **Zero-shot:** No examples, just the final definition and question.
- **Random Coord Baseline:** To check if the model is just hallucinating valid-looking coordinates.

### Evaluation Metrics
- **Addressing Accuracy:** Euclidean distance between predicted and ground truth coordinates (normalized).
- **Spatial Reasoning Accuracy:** Binary accuracy (Yes/No) for relative position queries.

### Statistical Analysis Plan
- T-tests to compare accuracy at different repetition levels.
- Regression analysis to find the "phase transition" point.

## Expected Outcomes
We expect a significant improvement in both addressing and reasoning accuracy as repetitions increase, with a potential "jump" around $N=3$.

## Timeline and Milestones
- **Hour 1:** Environment setup and data parsing.
- **Hour 2:** Implementation of prompting pipeline and Experiment 1.
- **Hour 3:** Experiment 2 and Error Analysis.
- **Hour 4:** Final analysis and Documentation.

## Potential Challenges
- **Tokenization:** Coordinates might be tokenized in ways that obscure their numeric value.
- **Spatial Blindness:** Models might struggle with the "reasoning" part even if they can repeat the coordinates.

## Success Criteria
- Identification of a clear repetition threshold for addressability.
- Demonstration of (or failure of) zero-shot spatial reasoning on addressed novel geometries.
