from shodak.models.style import StyleDocument, StyleDocumentType
from shodak.style.retriever import retrieve_style_examples


def test_retrieve_relevant_blog_example():
    documents=[
        StyleDocument(
            title="AI Blog",
            document_type=StyleDocumentType.blog,
            content=(
                "Artificial Intelligence systems are becoming easier to use. "
                "AI tools can simplify complex workflows."
            )
        ),
        StyleDocument(
            title="Travel blog",
            document_type=StyleDocumentType.blog,
            content="Travelling through the mountains is a completely different experience."
        )
    ]

    results=retrieve_style_examples(documents=documents,query="AI Systems and workflows", document_type=StyleDocumentType.blog, limit=1)

    assert len(results)==1
    assert "Artificial Intelligence" in results[0]



def test_retrieval_respects_document_type():
    documents=[
        StyleDocument(
            title="Research Paper",
            document_type=StyleDocumentType.research_paper,
            content="Artificial Intelligence models were experimentally evaluated."
        ),
        StyleDocument(
            title="Blog",
            document_type=StyleDocumentType.blog,
            content="I enjoy explaining artifical intelligence through examples."
        )
    ]
    results=retrieve_style_examples(
        documents=documents,
        query="artificial intelligence",
        document_type=StyleDocumentType.blog
    )

    assert len(results)==1
    assert "I enjoy explaining" in results[0]


def test_no_matching_examples_returns_empty():
    documents=[
        StyleDocument(
            title="Travel Blog",
            document_type=StyleDocumentType.blog,
            content="Mountains and rivers make long journeys."
        )
    ]

    results=retrieve_style_examples(
        documents=documents,
        query="machine learning",
        document_type=StyleDocumentType.research_paper
    )

    assert results==[]