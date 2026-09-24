import re

from shodak.models.style import StyleDocument, StyleDocumentType
from shodak.style.preprocessor import chunk_style_document


def _tokenize(text:str)->set[str]:
    return {
        word.lower() for word in re.findall(r"\b\w+\b",text)
        if len(word)>3
    }


def retrieve_style_examples(
        documents:list[StyleDocument],
        query:str,
        document_type:StyleDocumentType,
        limit:int=3
)->list[str]:
    query_words=_tokenize(query)
    scored_chunks:list[tuple[int,str]]=[]

    for document in documents:
        if document.document_type != document_type:
            continue
        chunks=chunk_style_document(document)
        for chunk in chunks:
            chunk_words=_tokenize(chunk)
            score=len(query_words&chunk_words)
            scored_chunks.append((score,chunk))
    scored_chunks.sort(
        key=lambda item: item[0], reverse=True
    )
    return [chunk for score,chunk in scored_chunks[:limit] if score>0]