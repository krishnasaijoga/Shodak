from shodak.graph.state import ShodakState
from shodak.style.corpus import load_style_corpus
from shodak.style.mapping import get_style_document_type
from shodak.style.profile import build_style_profiles_by_type
from shodak.style.retriever import retrieve_style_examples

STYLE_CORPUS_PATH="data/style_samples"

def style_context_node(state:ShodakState)->ShodakState:
    writing_request=state["writing_request"]
    research_request=state["research_request"]

    documents=load_style_corpus(STYLE_CORPUS_PATH)

    document_type=get_style_document_type(
        writing_request.output_type
    )
    profiles=build_style_profiles_by_type(documents)
    profile=profiles.get(document_type)
    examples=retrieve_style_examples(
        documents=documents,
        query=research_request.topic,
        document_type=document_type,
        limit=3
    )
    return {
        "style_document_type":document_type,
        "style_profile":profile,
        "style_examples":examples
    }