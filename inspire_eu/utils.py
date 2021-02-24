from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_inspire_eu_base_model(inspire_base_model=None):
    """
    Return the Base Model
    """

    if inspire_base_model is None:
        inspire_base_model = settings.INSPIRE_EU_BASE_MODEL

    try:
        module_name, class_name = inspire_base_model.rsplit(".", 1)
        _models = __import__(module_name, fromlist="*")
        try:
            return getattr(_models, class_name)
        except AttributeError as e1:
            raise ImproperlyConfigured(f"{inspire_base_model}: {e1}")
    except AttributeError as e2:
        raise ImproperlyConfigured(f"{inspire_base_model}: {e2}")
    except ModuleNotFoundError as e3:
        raise ImproperlyConfigured(f"{inspire_base_model}: {e3}")
