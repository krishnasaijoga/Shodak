from shodak.models.writing import OutputType

WRITING_TEMPLATES={
    OutputType.linkedin:[
        "Hook",
        "Context",
        "Key Insight",
        "Evidence",
        "Takeaway"
    ],
    OutputType.blog:[
        "Introduction",
        "Background",
        "Key Findings",
        "Discussion",
        "Conclusion"
    ],
    OutputType.academic:[
        "Introduction",
        "Evidence Review",
        "Critical Discussion",
        "Limitations",
        "Conclusion"
    ],
    OutputType.thesis:[
        "Background",
        "Literature Review",
        "Evidence Syntthesis",
        "Research Gap",
        "Conclusion"
    ]
}


def get_writing_template(output_type:OutputType)->list[str]:
    return WRITING_TEMPLATES[output_type]