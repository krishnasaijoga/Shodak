def normalize_doi(doi:str|None)->str|None:
    if not doi:
        return None
    normalized=doi.strip().lower()
    PREFIXES=[
        "https://doi.org/",
        "doi:",
        "DOI:",
        "http://doi.org/"
    ]
    for prefix in PREFIXES:
        if normalized.startswith(prefix):
            normalized=normalized.removeprefix(prefix).strip()
    return normalized or None