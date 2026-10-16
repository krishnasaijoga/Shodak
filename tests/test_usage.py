from types import SimpleNamespace

from shodak.usage import UsageTracker, extract_token_usage


def test_usage_tracker_records_calls():
    tracker=UsageTracker()

    tracker.record_call(
        provider="groq",
        prompt_tokens=100,
        completion_tokens=50
    )

    usage=tracker.providers["groq"]

    assert usage.calls==1
    assert usage.prompt_tokens==100
    assert usage.completion_tokens==50
    assert usage.total_tokens==150


def test_usage_tracker_records_retry():
    tracker=UsageTracker()
    tracker.record_retry("groq")
    assert tracker.providers["groq"].retries==1


def test_extract_usage_metadata():
    response=SimpleNamespace(
        usage_metadata={
            "input_tokens":120,
            "output_tokens":40
        }
    )

    prompt, completion=extract_token_usage(response)

    assert prompt==120
    assert completion==40


def test_extract_response_metadata():
    response=SimpleNamespace(
        usage_metadata=None,
        response_metadata={
            "token_usage":{
                "prompt_tokens":80,
                "completion_tokens":20
            }
        }
    )

    prompt, completion=extract_token_usage(response)

    assert prompt==80
    assert completion==20


def test_missing_usage_metadata_returns_zero():
    response=SimpleNamespace()

    assert extract_token_usage(response)==(0,0)