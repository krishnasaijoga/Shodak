# Shodak

Shodak is a multi-agent AI system for evidence-grounded research and personalized writing.

It separates research, evidence extraction, writing, evaluation, and revision into distinct stages so generated content remains grounded in retrieved evidence rather than relying only on model knowledge.

## Architecture

Shodak is built around three primary layers:

- Research Agent
- Writer Agent
- Evaluation Layer

These layers are orchestrated through a LangGraph-based workflow.

### Research Agent

The Research Agent is responsible for:

- research question generation
- academic source retrieval
- source normalization
- deduplication
- low-value source filtering
- source ranking
- abstract and metadata enrichment
- evidence extraction
- contradiction detection
- research quality assessment
- structured synthesis

The current academic research pipeline uses sources including:

- Semantic Scholar
- Crossref
- OpenAlex

### Writer Agent

The Writer Agent converts verified research into structured content.

Supported output formats include:

- LinkedIn posts
- Blogs
- Academic writing
- Thesis sections

The writer does not independently perform research. It receives structured evidence from the research pipeline and generates content from that evidence.

### Evaluation Layer

The Evaluation Layer measures:

- grounding
- citation correctness
- hallucination safety
- style similarity
- format compliance
- research quality
- overall output quality

Low-quality outputs may enter a bounded revision loop.

If the underlying research evidence is insufficient, evaluation and revision are skipped and Shodak produces a cautious output instead.

## High-Level Workflow

```text
User Request
    ↓
Research Planner
    ↓
Source Retrieval
    ↓
Normalization
    ↓
Deduplication
    ↓
Filtering
    ↓
Ranking
    ↓
Source Enrichment
    ↓
Evidence Extraction
    ↓
Research Quality Gate
    ↓
Research Synthesis
    ↓
Writer
    ↓
Citation Grounding
    ↓
Structural Postprocessing
    ↓
Evaluation
    ↓
Optional Revision
    ↓
Renderer
    ↓
API / CLI
```

For a more detailed explanation, see:

`docs/architecture.md`

## Key Features

- Multi-agent research and writing workflow
- Multi-source academic research
- Structured evidence extraction
- Research-quality gating
- Source deduplication and ranking
- Metadata and abstract enrichment
- Contradiction detection
- Evidence-grounded writing
- Multiple writing formats
- Citation grounding
- Personalized writing-style support
- Automated output evaluation
- Bounded revision loop
- Groq primary LLM provider
- OpenAI fallback provider
- Retry and fallback mechanisms
- Rate limiting
- Concurrency controls
- Research caching
- Structured logging
- Run-history persistence
- Graceful degradation
- Startup validation
- FastAPI interface
- CLI interface
- Docker support
- Docker Compose support
- GitHub Actions CI

## Requirements

- Python 3.12
- uv
- Git

Docker is optional for local Python development but required for containerized deployment.

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd Shodak
```

Install dependencies:

```bash
uv sync
```

Create your local environment file from the provided template:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Add the required API keys to `.env`.

## Configuration

Shodak supports Groq as its primary LLM provider and OpenAI as an optional fallback.

Example:

```env
APP_ENV=development

LOG_LEVEL=INFO

LLM_PROVIDER=groq
LLM_FALLBACK_PROVIDER=openai

GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-120b

OPENAI_API_KEY=
OPENAI_MODEL=gpt-5-mini
```

Additional settings are available for:

- LLM retries
- research retries
- caching
- concurrent requests
- provider request intervals
- run-history persistence

See `.env.example` for the complete configuration.

A production configuration template is also available in:

```text
.env.production.example
```

## CLI

Check whether Shodak is configured correctly:

```bash
shodak check
```

Research a topic:

```bash
shodak research "retrieval augmented generation"
```

Run the complete research and writing workflow:

```bash
shodak run "retrieval augmented generation" --output-type blog
```

Supported output types include:

```text
linkedin
blog
academic
thesis
```

## API

Start the API locally:

```bash
uv run uvicorn shodak.api.app:app --host 0.0.0.0 --port 8000
```

Primary endpoints:

```text
GET  /
GET  /health
POST /research
POST /write
POST /run
```

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```

## Docker

Build the Docker image:

```bash
docker build -t shodak .
```

Run Shodak:

```bash
docker run --rm -p 8000:8000 --env-file .env shodak
```

Or use Docker Compose:

```bash
docker compose up --build
```

Stop the Compose deployment:

```bash
docker compose down
```

## Testing

Run the full test suite:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Shodak also uses GitHub Actions to automatically run linting and tests on pushes and pull requests.

## Reliability

Shodak includes several production-oriented reliability mechanisms:

- exponential retry policies
- transient error classification
- LLM provider fallback
- research-provider retry
- rate limiting
- concurrent request control
- caching
- startup validation
- graceful degradation
- safe persistence
- structured logging
- sanitized API errors

Optional components such as synthesis and evaluation can fail gracefully without necessarily terminating the entire workflow.

Critical components such as research, writing, and rendering remain fail-fast.

## Research Quality Gate

Research quality is evaluated before the full downstream writing workflow continues.

Quality assessment considers factors such as:

- number of usable sources
- number of extracted evidence items
- coverage of generated research questions

If evidence is insufficient:

- Shodak marks the research as insufficient
- the writer generates a cautious response
- evaluation is skipped
- revision is skipped

This prevents the system from polishing unsupported content when the underlying research is weak.

## LLM Provider Flow

```text
Shodak Component
        ↓
LLM Router
        ↓
Primary Provider — Groq
        ↓
Retry Policy
        ↓
Fallback Provider — OpenAI
        ↓
Deterministic Fallback
when supported
```

This allows Shodak to continue operating when individual providers encounter transient failures or rate limits.

## Project Structure

```text
Shodak/
├── .github/
│   └── workflows/
├── docs/
├── src/
│   └── shodak/
│       ├── api/
│       ├── evaluation/
│       ├── graph/
│       ├── llm/
│       ├── research/
│       ├── writing/
│       ├── cache.py
│       ├── observability.py
│       ├── persistence.py
│       ├── recovery.py
│       ├── settings.py
│       ├── startup.py
│       └── usage.py
├── tests/
├── .env.example
├── .env.production.example
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

## Design Philosophy

Shodak deliberately separates research from writing.

The research system determines:

> What evidence exists?

The writing system determines:

> How should that evidence be communicated?

The evaluation system determines:

> How well does the final output remain grounded, structured, and aligned with the requested style?

This separation makes the system easier to test, extend, evaluate, and debug while reducing unsupported generation.

## Development Status

Shodak has completed its core research, writing, orchestration, evaluation, API, CLI, reliability, Docker, and CI foundations.

Current work focuses on deployment readiness, documentation, portfolio presentation, and final production validation.