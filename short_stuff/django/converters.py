class ShortCodeConverter:
    """This can be plugged into Django by registering it as a URL Converter. See
    https://docs.djangoproject.com/en/2.2/_modules/django/urls/converters/ or the README for more information.
    """
    regex = r'[-a-zA-Z0-9_]{1,22}'

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value
