import io

from coua.config import init_config


class TestInitConfig:
    def test_init_config_junit_recognized(self):
        file = io.StringIO("")
        init_config(file, ["junit.xml"], "do178c")
        file.flush()
        assert "JUnit" in file.getvalue()

    def test_init_config_mode_set(self):
        file = io.StringIO("")
        init_config(file, [], "do178c")
        file.flush()
        assert 'mode = "do178c"' in file.getvalue()
