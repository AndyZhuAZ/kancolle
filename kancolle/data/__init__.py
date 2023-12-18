"""Data module."""
import importlib.resources
import os.path

try:
    MODULE_PATH = importlib.resources.files(__package__)
except AttributeError:
    MODULE_PATH = os.path.abspath(os.path.dirname(__file__))
KC_DATA_URL = "https://andychucs.github.io/kcwiki-kcdata/"
KC_QUEST_URL = "https://andychucs.github.io/kcQuest/"
