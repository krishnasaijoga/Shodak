from unittest.mock import patch

from shodak.persistence import (
    RunHistoryStore,
    RunRecord,
    persist_completed_run,
    try_persist_completed_run,
)


def test_run_history_append_and_load(tmp_path):
    path=tmp_path/"history.jsonl"
    store=RunHistoryStore(path)
    record=RunRecord(
        run_id="run-123",
        topic="retrieval augmented generation",
        output_type="blog",
        rendered_output="# Test",
        evaluation={
            "overall_quality_score":0.9
        },
        usage={
            "total_calls":2
        }
    )

    store.append(record)

    records=store.load_all()

    assert len(records)==1

    assert records[0].run_id=="run-123"
    assert records[0].topic=="retrieval augmented generation"


def test_run_history_preserves_multiple_runs(tmp_path):
    path=tmp_path/"history.jsonl"
    store=RunHistoryStore(path)
    store.append(
        RunRecord(
            run_id="run-1",
            topic="RAG",
            output_type="blog",
            rendered_output="First"
        )
    )
    store.append(
        RunRecord(
            run_id="run-2",
            topic="Transformers",
            output_type="linkedin",
            rendered_output="Second"
        )
    )

    records=store.load_all()

    assert len(records)==2
    assert records[0].run_id=="run-1"
    assert records[1].run_id=="run-2"


def test_missing_history_returns_empty_list(tmp_path):
    store=RunHistoryStore(tmp_path/"missing.jsonl")
    assert store.load_all()==[]


def test_persist_completed_run(tmp_path):
    history_path=tmp_path/"history.jsonl"

    with (
        patch(
            "shodak.persistence.settings.run_history_enabled",
            True
        ),
        patch(
            "shodak.persistence.settings.run_history_path",
            str(history_path)
        ),
        patch(
            "shodak.persistence.get_usage_summary",
            return_value={
                "total_calls":2,
                "total_retries":1
            }
        )
    ):
        record=persist_completed_run(
            topic="RAG",
            output_type="blog",
            rendered_output="# Output",
            evaluation={
                "overall_quality_score": 0.9,
            }
        )

    assert record is not None
    assert record.topic=="RAG"

    store=RunHistoryStore(history_path)

    records=store.load_all()

    assert len(records)==1
    assert records[0].usage["total_calls"]==2


def test_persistence_can_be_disabled(tmp_path):
    history_path=tmp_path/"history.jsonl"

    with patch(
        "shodak.persistence.settings.run_history_enabled",
        False
    ):
        record=persist_completed_run(
            topic="RAG",
            output_type="blog",
            rendered_output="# Output",
            evaluation=None
        )

    assert record is None
    assert history_path.exists() is False


def test_persistence_failure_is_recoverable():
    with patch(
        "shodak.persistence.persist_completed_run",
        side_effect=OSError("Disk unavailable")
    ):
        result=try_persist_completed_run(
            topic="RAG",
            output_type="blog",
            rendered_output="# Output",
            evaluation=None
        )

    assert result is None