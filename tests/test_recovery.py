from shodak.recovery import run_optional


def test_optional_operation_success():
    result=run_optional(
        lambda: "success",
        operation_name="test",
        fallback="fallback"
    )

    assert result=="success"


def test_optional_operation_uses_fallback():
    def fail():
        raise RuntimeError("failure")

    result=run_optional(
        fail,
        operation_name="test",
        fallback="fallback"
    )

    assert result=="fallback"