from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from shodak.config import settings
from shodak.usage import get_usage_summary


class RunRecord(BaseModel):
    run_id:str
    created_at:datetime=Field(default_factory=lambda: datetime.now(UTC))
    topic:str
    output_type:str
    rendered_output:str
    evaluation:dict[str,Any]|None=None
    usage:dict[str,Any]|None=None


class RunHistoryStore:
    def __init__(self,path:Path)->None:
        self.path=path

    
    def append(self,record:RunRecord)->None:
        self.path.parent.mkdir(parents=True,exist_ok=True)

        with self.path.open("a",encoding="utf-8") as file:
            file.write(record.model_dump_json())
            file.write("\n")

    
    def load_all(self)->list[RunRecord]:
        if not self.path.exists():
            return []

        records:list[RunRecord]=[]

        with self.path.open("r",encoding="utf-8") as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                records.append(RunRecord.model_validate_json(line))
        return records


def persist_completed_run(
        *,
        topic:str,
        output_type:str,
        rendered_output:str,
        evaluation:dict[str,Any]|None
)->RunRecord|None:
    if not settings.run_history_enabled:
        return None

    record=RunRecord(
        run_id=str(uuid4()),
        topic=topic,
        output_type=output_type,
        rendered_output=rendered_output,
        evaluation=evaluation,
        usage=get_usage_summary()
    )
    store=RunHistoryStore(Path(settings.run_history_path).expanduser())

    store.append(record)

    return record