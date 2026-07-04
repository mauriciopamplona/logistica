from pathlib import Path
import yaml

class Config:

    def __init__(self):

        config_path = Path("configs/config.yaml")

        with config_path.open() as f:
            self._config = yaml.safe_load(f)

    @property
    def application(self):
        return self._config["application"]

    @property
    def spark(self):
        return self._config["spark"]

    @property
    def paths(self):
        return self._config["paths"]

    @property
    def output(self):
        return self._config["output"]