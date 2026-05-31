# Literature Review: Addressability of Repeated Novel Geometries

## Research Area Overview
This literature review explores the intersection of in-context learning (ICL), spatial reasoning, and symbolic representation in large language models (LLMs). The core question is whether LLMs can learn to "address" (refer to) novel 2D geometries through prompting, especially when these geometries are repeated.

## Key Papers

### 1. Beyond Lines and Circles: Unveiling the Geometric Reasoning Gap (2024)
- **Authors**: Spyridon Mouselinos et al.
- **Key Contribution**: Identifies significant gaps in LLMs' ability to reason about 2D spatial relationships.
- **Methodology**: Evaluates LLMs on constructive geometric problems and multi-agent systems for self-correction.
- **Relevance**: Establishes the baseline difficulty LLMs face with geometric "perception" and reasoning.

### 2. TangramPuzzle: Evaluating Multimodal LLMs with Compositional Spatial Reasoning (2026)
- **Authors**: Daixian Liu et al.
- **Key Contribution**: Introduces a benchmark using Tangram puzzles and a symbolic framework (TCE) for exact coordinate specifications.
- **Relevance**: Provides a method for grounding geometries in machine-verifiable coordinates, which is crucial for "addressing" geometries.

### 3. In-Context Learning Operates as Concept Subspace Learning (2026)
- **Authors**: Wei Tang et al.
- **Key Contribution**: Proposes that task-relevant information in ICL is concentrated in low-dimensional activation subspaces.
- **Relevance**: Suggests a mechanistic explanation for how "repeated" tasks or geometries might be represented and retrieved efficiently in-context.

### 4. The Lattice Representation Hypothesis (2026)
- **Authors**: Bojian Xiong
- **Key Contribution**: Argues that LLMs use linear attribute directions to encode concept lattices.
- **Relevance**: Provides a theoretical framework for how symbolic names (labels) could be grounded in geometric/latent space.

### 5. Abstract Visual Reasoning with Tangram Shapes (KiloGram) (2022)
- **Authors**: Anya Ji et al.
- **Key Contribution**: Large-scale dataset of tangram descriptions and part-level segmentations.
- **Relevance**: Provides the "novel geometries" and their corresponding verbal "addresses" (names for parts and whole shapes).

## Common Methodologies
- **Symbolic Grounding**: Using coordinates (SVG, TCE) or domain-specific languages (DSL) to represent geometry.
- **In-Context Learning (ICL)**: Presenting examples in the prompt to induce task performance without weight updates.
- **Mechanistic Interpretability**: Analyzing activation subspaces or "induction heads" to understand how ICL works.

## Gaps and Opportunities
- **Limited Repetition**: Most studies focus on many-shot or zero-shot, but the impact of *limited repetition* of a *novel* geometry is less explored.
- **Verbal vs. Geometric Addressing**: Can a model transition from coordinate-based addressing to purely verbal addressing once a geometry is "named" in-context?

## Recommendations for Our Experiment
- **Dataset**: Use the Tangram/KiloGram SVG definitions as "novel geometries".
- **Baselines**: Compare performance when geometries are referred to by coordinates vs. by assigned names.
- **Metrics**: Accuracy in identifying parts or properties of the geometry after it has been defined and repeated in-context.
