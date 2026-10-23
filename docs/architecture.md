# Shodak Architecture

## Overview

Shodak is a multi-agent research and writing system designed to:
1. research a topic from multiple source types
2. extract and synthesize evidence.
3. generate grounded lon-form content
4. evaluate output quality
5. revise when required

## High-Level Flow

User Request
-> Research Planner
-> Source Retrieval
-> Source Normalization
-> Deduplication
-> Filtering
-> Ranking
-> Enrichment
-> Evidence Extraction
-> Research Quality Evaluation
-> Research Synthesis
-> Writer
-> Citation Grounding
-> Structural Postprocessing
-> Evaluation
-> Optional Revision
-> Renderer
-> API / CLI Output

## Core Components

### Research Layer
Responsible for:
- research question planning
- academic source retrieval
- source normalization
- deduplication
- relevance filtering
- ranking
- metadata/abstract enrichment
- evidence extraction
- contradiction detection
- research quality assesment

### Evidence Layer
Converts retrieved sources into structured evidence used by downstream components.

The writer should only use evidence provided by the research pipeline.

### Synthesis Layer
Produces structured research synthesis from the collected evidence.

Synthesis is treated as an optional component and can gracefully fall back if an LLM response cannot be validated.

### Writing Layer
Supports multiple output formats
- LinkedIn
- Blog
- Thesis
- Academic

The writer receives the research report and does not independently retrieve new information.

### Citation Grounding
Ensures claims generated in the draft remain connected to supporting evidence.

### Structural Postprocessing
Enforces deterministic structural requirements that should not depend entirely on LLM behavior.

Examples include contradiction-handling sections where applicable.

### Evaluation Layer
Evaluates:
- grounding
- citation correctness
- hallucination safety
- style similarity
- format comliance
- research quality
- overall quality

Evaluation is skipped when research evidence is insufficient.

### Revision Layer
Low-quality drafts may be revised within a bounded revision loop.

Revision is skipped when the underlying research evidence is insufficient.

### Rendering Layer
Converts the final structured draft into user-facing output.

## LLM Provider Architecture

Shodak supports:

- Groq as the primary provider
- OpenAI as an optional fallback provider

Provider flow:

Component
-> LLM Router
-> Primary Provider
-> Retry Policy
-> Fallback Provider
-> Deterministic Fallback where supported

## Reliability Features

Shodak includes:

- retry policies
- provider fallback
- rate limiting
- concurrency limiting
- caching
- graceful degradation
- strcutured logging
- startup validation
- run persistence
- sanitized error handling

## Research Quality Gate

Research quality is evaluated before downstream generation.

Factors include:
- number of sources
- number of evidence items
- research-question coverage

If evidence is insufficient:
- the writer produces a cautious output
- evaluation is skipped
- revision is skipped

## Interfaces

Shodak provides:

### CLI
Examples:

```bash
shodak research "retrieval augmented generation"
shodak run "retrieval augmented generation" --output-type blog
shodak check
```

## API

### Primary Endpoints
GET /
GET /health
POST /research
POST /write
POST /run

## Deployment
Shodak can run:
- locally through Python/uv
- inside Docker
- using Docker Compose
- in CI through GitHub Actions

## Design Principle
Research and writing responsibilities remain separated.

The research system determines what evidence exists.

The writing system determines how that evidence should be communicated.

This separation reduces unsupported generation and makes the system easier to evaluate, test, and extend.