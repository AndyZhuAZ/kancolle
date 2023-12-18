"""Data module."""
import importlib.resources

MODULE_PATH = importlib.resources.files(__package__)
# only on python >= 3.9, see https://docs.python.org/3/library/importlib.resources.html
# MODULE_PATH = os.path.abspath(os.path.dirname(__file__)) for python < 3.9
KC_DATA_URL = "https://andychucs.github.io/kcwiki-kcdata/"
KC_QUEST_URL = "https://andychucs.github.io/kcQuest/"
