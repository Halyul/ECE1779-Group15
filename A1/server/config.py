import pathlib
import yaml

class Config:

    def __init__(self, config="config.yaml"):
        """
            self.path: config path
            self.config: system config
        """
        self.path = pathlib.Path.cwd().joinpath(config)
        self.config = yaml.safe_load(open(self.path, "r"))
    
    def fetch(self):
        """
            This method provides the configuration of the system
            Args:
                self: access global variables
            Returns:
                str: system config
        """
        return self.config