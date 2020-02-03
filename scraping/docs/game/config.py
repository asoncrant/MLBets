import json
from ..config import Config

class gameConfig(Config):
    """Game web-scraping configuration class."""

    def __init__(self, config):
        self._config = config['games']

    @property
    def url(self):
        return self.get_property('url')

    @property
    def years(self):
        return self.get_property("years")

    @property
    def weeks(self):
        return self.get_property("weeks")

    @property
    def wait(self):
        return self.get_property("wait")
