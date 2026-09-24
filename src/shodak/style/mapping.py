from shodak.models.style import StyleDocumentType
from shodak.models.writing import OutputType

OUTPUT_STYLE_MAP={
    OutputType.linkedin:StyleDocumentType.linkedin,
    OutputType.blog:StyleDocumentType.blog,
    OutputType.academic:StyleDocumentType.research_paper,
    OutputType.thesis:StyleDocumentType.research_paper
}



def get_style_document_type(
        output_type:OutputType
)->StyleDocumentType:
    return OUTPUT_STYLE_MAP[output_type]