from django.utils import crypto
HASH_MAX_LENGTH = 8


def create_hash():
    return crypto.get_random_string(HASH_MAX_LENGTH)


def get_unique_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except:
        return None
