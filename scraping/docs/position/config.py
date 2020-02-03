import json
from ..config import Config

class posnConfig(Config):
    """Web scraping configuration object"""

    def __init__(self, config):
        self._config = config['positions']

    @property
    def url(self):
        return self.get_property('url')

    @property
    def table_class(self):
        return self.get_property('table_class')

    @property
    def years(self):
        return self.get_property('years')

    @property
    def weeks(self):
        return self.get_property('weeks')

    @property
    def pos_ids(self):
        return self.get_property('pos_ids')

    @property
    def wait(self):
        return self.get_property('wait')
