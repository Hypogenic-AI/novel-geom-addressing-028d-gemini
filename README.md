# Addressability of Repeated Novel Geometries

This project investigates the in-context learning of 2D geometries in Large Language Models. Specifically, it tests whether models can map verbal labels to coordinate-defined shapes and if repetition improves their ability to reason about these shapes.

## Key Findings
- **High Addressability:** Models like GPT-4o achieve 100% accuracy in retrieving coordinates for named parts with as little as 0-1 examples in the prompt.
- **Limited Spatial Reasoning:** Despite perfect retrieval, spatial reasoning (e.g., "Is part A above part B?") is poor (~60-80%) and does not significantly benefit from repetition in the 1-20 shot range.
- **Independence of Semantics:** The use of novel nonsense names for shapes and parts did not significantly decrease accuracy, indicating that the model relies on coordinate processing rather than just semantic priors.

## Repository Structure
- `src/`: Python scripts for data preprocessing, experimentation, and analysis.
- `results/`: Processed data, experimental results (JSON), and plots.
- `REPORT.md`: Detailed research report.
- `planning.md`: Initial research plan and motivation.

## How to Reproduce
1. Install dependencies: `uv add openai anthropic numpy pandas matplotlib scipy python-dotenv`
2. Run preprocessing: `python src/preprocess_data.py`
3. Run experiments: `python src/experiment.py`, `src/experiment_scaling.py`, etc.
4. Run analysis: `python src/analyze_results.py`

## Credits
This research utilizes the KiloGram dataset and is inspired by recent findings in in-context representation learning (arXiv:2501.00070).
