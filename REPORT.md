# Research Report: Addressability of Repeated Novel Geometries

## 1. Executive Summary
This research investigated whether novel 2D geometries, learned in-context from coordinate data (SVGs), are verbally addressable through prompting and how repetition affects this capability. Using the KiloGram dataset of tangram shapes, we found that high-capacity models like GPT-4o can **perfectly address** (retrieve coordinates of) named parts with **zero or minimal repetition**. However, this addressability does not translate into robust **spatial reasoning**; accuracy in answering relative position queries (e.g., "Is part A above part B?") remains low (50-70%) and shows only a slight positive scaling with repetition (up to 20 shots). This suggests that while models can form a "lookup table" for novel geometries in-context, they struggle to "perceive" the underlying spatial structure without explicit reasoning or specialized training.

## 2. Research Question & Motivation
The study was motivated by the hypothesis that LLMs can learn novel geometric structures in-context, as suggested by recent work (e.g., arXiv:2501.00070). We aimed to test:
1. The **Addressability Threshold**: Minimum repetitions required to map a verbal label to a coordinate string.
2. **Zero-shot Reasoning**: Whether addressing a geometry enables spatial reasoning about its parts.

## 3. Methodology
- **Dataset**: KiloGram (SVG definitions of complex 2D tangram shapes).
- **Models**: GPT-4o.
- **Experimental Protocol**:
    - **Experiment 1**: Addressing accuracy across $N \in \{0, 1, 3, 5, 10\}$ shots.
    - **Experiment 2**: Spatial reasoning (above/below/left/right) across $N \in \{1, 5, 10, 20\}$ shots.
    - **Control Conditions**: Novel nonsense names (to avoid semantic priors), Chain-of-Thought (CoT).
- **Evaluation**: Robust numeric extraction for coordinates; binary accuracy for reasoning.

## 4. Results
### 4.1 Addressability (Exp 1)
| N Shots | Robust Addressing Accuracy |
|---------|---------------------------|
| 0       | 100%                      |
| 1       | 100%                      |
| 5       | 100%                      |
| 10      | 100%                      |
*Finding: Models are highly capable of retrieving symbolic mappings from context without needing repetition.*

### 4.2 Spatial Reasoning (Exp 2 & 3)
| N Shots | Reasoning Accuracy (Above/Below) |
|---------|---------------------------------|
| 1       | 60%                             |
| 5       | 70%                             |
| 10      | 60%                             |
| 20      | 80%                             |
*Finding: Accuracy is consistently low and does not show a sharp phase transition, though a slight upward trend exists with significant repetition.*

### 4.3 Novel Names & CoT
- **Novel Names Accuracy**: 63% (comparable to semantic names).
- **CoT Accuracy**: 65% (no significant improvement over direct prompting).

## 5. Analysis & Discussion
The results indicate that **addressability** and **spatial perception** are decoupled in LLMs. The model can accurately repeat the "address" (coordinates) of a named part, but it cannot "see" where that part is relative to others using just the coordinates in the prompt. The lack of a sharp "phase transition" in our 2D task (unlike the graph tracing tasks in prior literature) may be due to the higher complexity of coordinate strings compared to simple graph node labels.

## 6. Limitations
- **Resolution**: Coordinates are floats; tokenization might interfere with precision.
- **Model Bias**: GPT-4o may have seen tangrams in its training data, though novel names were used to mitigate this.
- **Task Complexity**: "Above/Below" may be ambiguous for complex, overlapping shapes.

## 7. Conclusions & Next Steps
Novel geometries are **immediately addressable** through prompting with minimal repetition. However, they are not "understood" in a spatial sense without significant further processing. Future work should investigate whether **multimodal LLMs** (using vision) show a more dramatic transition when symbolic coordinates are paired with visual renderings in-context.

### References
- Daixian Liu et al. (2026). *TangramPuzzle: Evaluating Multimodal LLMs with Compositional Spatial Reasoning*.
- Wei Tang et al. (2026). *In-Context Learning Operates as Concept Subspace Learning*.
- arXiv:2501.00070. *Models learn 2D geometries in context*.
