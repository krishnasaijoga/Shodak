import json
from pathlib import Path

from shodak.models.style import StyleDocumentType
from shodak.style.profile import StyleProfile


def save_style_profile(
        profiles:dict[StyleDocumentType,StyleProfile],
        file_path:str|Path
)->None:
    path=Path(file_path)
    data={
        document_type.value: profile.model_dump() for document_type,profile in profiles.items()
    }
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(
            json.dumps(
                data,
                indent=2
            ),
        encoding="utf-8"
    )



def load_style_profile(
        file_path:str|Path
)->dict[StyleDocumentType,StyleProfile]:
    path=Path(file_path)
    if not path.exists():
        return {}
    data=json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )
    return {
        StyleDocumentType(document_type): StyleProfile(**profile_data) for document_type,profile_data in data.items()
    }