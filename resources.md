# Resources Catalog: Novel Geometry Addressing

## Summary
This document catalogs all resources gathered for the research project "Are repeated novel geometries addressable without reasoning?".

## Papers
Total papers downloaded: 5

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Beyond Lines and Circles | Spyridon Mouselinos et al. | 2024 | papers/2402.04351_beyond_lines.pdf | Geometric reasoning gaps in LLMs |
| TangramPuzzle | Daixian Liu et al. | 2026 | papers/2407.12781_tangram_puzzle.pdf | Coordinate-based tangram benchmark |
| Minimization of Boolean Complexity | Leroy Z. Wang et al. | 2024 | papers/2410.19702_boolean_complexity.pdf | Simplicity bias in ICL |
| In-Context Learning Subspaces | Wei Tang et al. | 2026 | papers/2410.01211_concept_subspace.pdf | Mechanistic view of ICL |
| The Geometry of Reasoning | Yufa Zhou et al. | 2025 | papers/2409.05432_geometry_reasoning.pdf | Reasoning as flows in representation space |

See papers/README.md for more details.

## Datasets
Total datasets gathered: 2

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| Tangram | GitHub (yizhouzhao) | ~700 items | Shape replication | code/Tangram/ | Abstract diagrams and human solutions |
| KiloGram | GitHub (lil-lab) | >1k stimuli | Visual reasoning | code/kilogram/ | Rich part-level annotations and SVGs |

See datasets/README.md for download and loading instructions.

## Code Repositories
Total repositories cloned: 2

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| Tangram | https://github.com/yizhouzhao/Tangram | Dataset access | code/Tangram/ | Contains tangram images and data |
| KiloGram | https://github.com/lil-lab/kilogram | Dataset access | code/kilogram/ | Contains SVG definitions and labels |

## Recommendations for Experiment Design

1. **Primary dataset**: **KiloGram** (specifically the SVG definitions in `dataset/tangrams-svg/`). These provide precise 2D coordinates for novel geometries.
2. **Baseline methods**: 
   - Zero-shot (no repetition) vs. Few-shot (repeated novel geometry).
   - Coordinate-based prompts (addressing by points) vs. Name-based prompts (addressing by assigned verbal labels).
3. **Evaluation metrics**:
   - Accuracy of part identification (e.g., "What is the coordinate of the 'head'?").
   - Consistency across different "addresses" for the same geometry.
4. **Code to adapt**:
   - Use the SVG parsing logic from the `kilogram` repo or standard XML parsers to extract coordinates for prompting.
