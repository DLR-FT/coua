import io
import tomllib

from coua.config import init_config


class TestInitConfig:
    def test_init_config_junit_recognized(self):
        file = io.StringIO("")
        init_config(file, ["junit.xml"], ["do178c"])
        file.flush()
        assert "JUnit" in file.getvalue()

    def test_init_config_mode_set(self):
        file = io.StringIO("")
        init_config(file, [], ["do178c"])
        file.flush()
        cfg = tomllib.loads(file.getvalue())
        assert "checks" in cfg
        assert "do178c" in cfg["checks"]["suites"]
