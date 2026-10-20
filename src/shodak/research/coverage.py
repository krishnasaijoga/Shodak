from shodak.models.evidence import Evidence


GENERIC_RESEARCH_WORDS={
    "machine",
    "learning",
    "model",
    "models",
    "method",
    "methods",
    "system",
    "systems",
    "research",
    "study",
    "studies",
    "approach",
    "approaches",
    "data"
}

def _tokenize(text:str)->set[str]:
    return {
        word.strip(".,!?()[]{}:;\"'").lower() for word in text.split()
        if (
            len(word)>3
            and word.strip(".,!?()[]{}:;\"'").lower() not in GENERIC_RESEARCH_WORDS
        )
    }


def question_is_covered(question:str,evidence_items:list[Evidence],minimum_overlap:int=2,minimum_ratio:float=0.25)->bool:
    question_words=_tokenize(question)
    if not question_words:
        return False
    for evidence in evidence_items:
        evidence_words=_tokenize(evidence.claim)
        overlap=question_words & evidence_words
        overlap_ratio=len(overlap)/len(question_words)
        if len(overlap)>=minimum_overlap and overlap_ratio>=minimum_ratio:
            return True
    return False


def calculate_research_coverage(questions:list[str],evidence_items:list[Evidence])->float:
    if not questions:
        return 0.0
    covered=sum(question_is_covered(question,evidence_items) for question in questions)
    return covered/len(questions)