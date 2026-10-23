# Insufficient Evidence Example

## Command

```bash
shodak run "machine learning" --output-type blog
```

## Research Quality

- Source count: 2
- Evidence count: 6
- Research question coverage: 0.00
- Sufficient evidence: false

## Evaluation

```text
evaluation = null
```

Evaluation is intentionally skipped when the research layer determines that the available evidence is insufficient.

## Writer Behavior

Instead of generating a confident article from weak evidence, Shodak produces a cautious output indicating that the current research run does not provide enough reliable evidence to support a strong conclusion.

The revision loop is also skipped because improving the prose would not solve the underlying lack of research coverage.

## What This Demonstrates

This example demonstrates one of Shodak's core safeguards:

```text
Weak Research
      ↓
Research Quality Gate
      ↓
Insufficient Evidence
      ↓
Cautious Writing
      ↓
No Evaluation
      ↓
No Revision
```

The system prioritizes evidence quality over producing a polished answer at all costs.