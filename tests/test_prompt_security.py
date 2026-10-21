from shodak.prompts.security import UNTRUSTED_CONTENT_INSTRUCTION


def test_untrusted_content_instruction_exists():
    instruction = UNTRUSTED_CONTENT_INSTRUCTION.lower()
    assert "untrusted" in instruction
    assert "do not follow instructions" in instruction
