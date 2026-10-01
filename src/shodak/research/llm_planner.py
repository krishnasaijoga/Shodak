from pydantic import BaseModel, Field

from shodak.llm.factory import get_llm
from shodak.models.research import ResearchRequest


class ResearchPlan(BaseModel):
    questions:list[str]=Field(min_length=3,max_length=12)


def build_llm_research_questions(
        request:ResearchRequest
)->list[str]:
    llm=get_llm().with_structured_output(ResearchPlan)
    prompt=f"""
You are a research planning assistant.

Break the following topic into focused research questions.

Topic:
{request.topic}

Research depth:
{request.depth.value}

Requirements:
- Questions must be specific and non-overlapping.
- Cover definition, mechanism, evidence, limitations, and recent developments.
- Include acdemic or peer-reviewed evidence when relevant.
- Include official or regulatory perspectives when relevant.
- Include practitioner or community perspective when relevant.
- Do not answer the question.
- Return only structured output.
"""
    result=llm.invoke(prompt)
    return result.questions