# To test the config file working

from shodak.config import settings


def test_default_app_name():
    assert settings.app_name == "shodak"


def test_environment_is_loaded():
    assert settings.environment


def test_log_level_is_loaded():
    assert settings.log_level