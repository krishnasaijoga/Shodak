import re

from shodak.models.style import StyleDocument


def clean_style_text(text:str)->str:
    text=text.strip()
    text=re.sub(r"\r\n?","\n",text)
    text=re.sub(r"[ \t]+"," ",text)
    text=re.sub(r"\n{3,}","\n\n",text)
    return text


def chunk_style_document(
        document:StyleDocument,
        chunk_size:int=800,
        overlap: int=100
)->list[str]:
    text=clean_style_text(document.content)
    if not text:
        return []
    if chunk_size<=0:
        raise ValueError(f"Chunk size: {chunk_size} cannot be less than or equal to 0")
    if overlap <0 or overlap>=chunk_size:
        raise ValueError(f"Overalp: {overlap} cannot be less than or equal to zero or greater than the chunk size: {overlap}")

    chunks:list[str]=[]

    start =0
    while start<len(text):
        end=start+chunk_size
        chunk=text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end>=len(text):
            break
        start=end-overlap
    return chunks