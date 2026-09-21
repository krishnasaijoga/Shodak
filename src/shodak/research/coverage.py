from shodak.models.evidence import Evidence


def _tokenize(text:str)->set[str]:
    return {
        word.strip(".,!?()[]{}:;\"'").lower() for word in text.split() if len(word)>3
    }


def question_is_covered(question:str,evidence_items:list[Evidence],minimum_overlap:int=2)->bool:
    question_words=_tokenize(question)
    for evidence in evidence_items:
        evidence_words=_tokenize(evidence.claim)
        overlap=question_words & evidence_words
        if len(overlap)>=minimum_overlap:
            return True
    return False


def calculate_research_coverage(questions:list[str],evidence_items:list[Evidence])->float:
    if not questions:
        return 0.0
    covered=sum(question_is_covered(question,evidence_items) for question in questions)
    return covered/len(questions)