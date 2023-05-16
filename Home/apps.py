import pickle

from django.apps import AppConfig
from Home.load_model import load_model
from django.core.cache import cache


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Home'

    def ready(self):
        model = load_model()
        cache.set("random_forest_model", pickle.dumps(model))
