# Blog Example

## Command

```bash
shodak run "retrieval augmented generation" --output-type blog
```

## Evaluation Summary

- Grounding: 1.00
- Citation correctness: 1.00
- Hallucination safety: 1.00
- Style similarity: 0.24
- Format compliance: 1.00
- Research quality: 0.67
- Overall quality: 0.82

## What This Demonstrates

This example shows the complete Shodak workflow operating successfully from research through writing and evaluation.

The generated blog was:

- grounded in retrieved evidence
- fully supported by citations
- free from detected hallucination issues
- compliant with the requested blog format
- evaluated through the quality-scoring layer

The lower style-similarity score indicates that the output remained structurally and factually strong while still having room for improvement in matching the target writing style.

## Workflow

```text
Research
→ Evidence Extraction
→ Research Synthesis
→ Blog Generation
→ Citation Grounding
→ Structural Postprocessing
→ Evaluation
→ Final Output
```