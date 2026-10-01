from shodak.models.research import ResearchRequest
from shodak.research.llm_planner import build_llm_research_questions


def build_research_questions(request: ResearchRequest)->list[str]:
    topic=request.topic.strip()

    questions=[
        f"what is the {topic}?",
        f"what are the main concepts, methods, or technologies related to {topic}?",
        f"what are the main benefits and use cases of {topic}",
        f"what are the known limitations or criticisms of the {topic}?",
        f"what recent research or evidence exists about {topic}?"
    ]

    if request.include_official:
        questions.append(
            f"what do the official organizations, standard bodies, or regulators say about {topic}?"
        )
    if request.include_academic:
        questions.append(
            f"what does peer-reviewed papers and academic studies conculde about {topic}?"
        )
    if request.include_community:
        questions.append(
            f"what practical experiments or recurring issues are reported by practitioners regarding {topic}?"
        )

    if request.depth.value=="quick":
        return questions[:3]
    if request.depth.value=="standard":
        return questions[:6]
    return questions


def build_research_questions_with_fallback(
        request:ResearchRequest
)->list[str]:
    try:
        return build_llm_research_questions(request)
    except Exception: # noqa: BLE001
        return build_research_questions(request)