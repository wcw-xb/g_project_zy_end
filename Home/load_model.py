# load_model.py
import pickle
from django.conf import settings


def load_model():
    with open(settings.MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model
