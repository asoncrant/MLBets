class Config(object):
    """
    Base configuration class. Sub-classes will take in a dictionary and
    use it to set configuration properties for that sub-class.
    """

    def __init__(self, config=None):
        self._config = config

    def get_property(self, property_name):
        if property_name not in self._config.keys():
            return None  
        return self._config[property_name]
