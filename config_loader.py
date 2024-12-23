"""
ConfigLoader class that loads configuration from a file.
"""
import yaml


class ConfigLoader:
    """
    ConfigLoader is designed to load configurations from a YAML file.
    """
    def __init__(self, filepath):
        """
        Initialize the ConfigLoader with the file path of the configuration
        file.
        """
        self.filepath = filepath
        self.config = None

    def load_config(self):
        """
        Load configurations from the YAML file.
        """
        try:
            with open(self.filepath, 'r') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Config file not found at {self.filepath}. \
                  Please check the file path.")
        except yaml.YAMLError as e:
            print(f"Error while parsing the config file: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

    def get_config(self):
        """
        Get the loaded configuration. If the configuration hasn't been loaded
        yet, load it first.
        """
        if not self.config:
            self.load_config()

        if self.config:
            return self.config
        else:
            print("Config could not be loaded.")
            return None
