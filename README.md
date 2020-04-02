# Short Stuff

By Fox at [Artconomy.com](https://artconomy.com/).

Short Stuff is a set of helper functions used for generating short unique identifiers, such as those used 
in YouTube video IDs or in URL shorteners.

Short Stuff does this by generating random byte strings, running them through base64 encoding and 
then doing some cleanup for compatibility.

Most distinct about the methodology is that it piggy-backs on UUIDs. That means that if you want to leverage your
database or library's native UUID support, you can do so, and helper functions are 
provided for this.

---

## Installation

Short Stuff requires (at least) Python 3.5. It has only been tested on Python 3.7. The tests use 
formatted strings, which were introduced in 3.6.

To install:

```
pip install short_stuff
```

## Quick Guide

To generate a short code:

```
>>> from short_stuff import gen_shortcode
>>> gen_shortcode()
'XtFxMb7qTJ-A'
```

To turn this code into a UUID (such as for DB storage):

```
>>> from short_stuff import unslugify
>>> unslugify('XtFxMb7qTJ-A')
UUID('5ed17131-beea-4c9f-8000-000000000000')
```

Notice that this is a truncated [UUID](https://docs.python.org/3/library/uuid.html), with everything beyond the first
eight bytes zeroed out.

To turn the UUID back into a slug:

```
>>> from uuid import UUID
>>> from short_stuff import slugify
>>> slugify(UUID('5ed17131-beea-4c9f-8000-000000000000'))
'XtFxMb7qTJ-A'
```


## Django

First class support for Django is provided. Django must be installed to use these features.
The ShortCodeField model field is provided and is a special wrapper around UUIDField.

```
from django.db import models
from short_stuff import gen_shortcode
from short_stuff.django.models import ShortCodeField


class Doohickey(models.Model):
    id = ShortCodeField(primary_key=True, db_index=True, default=gen_shortcode)

```

Note that in most cases you can pass UUIDs to the field and allow it to convert internally.
This might be helpful if converting existing models to use shortcodes. Migrations should go smoothly,
but please be sure to test!

**NOTICE**: Use `gen_shortcode` and not `gen_shortcode()`! if you don't omit the parentheses, the function
will evaluate during the class definition and Django will attempt to set ALL new rows for the table with
that default.

Now that you have the shortcodes on your models, you'll want to make it possible to refer to them in your URLs.

To do this, register the provided path converter:

```
from django.urls import path, register_converter
from short_stuff import ShortCodeConverter

from . import views

register_converter(converters.ShortCodeConverter, 'short_code')

urlpatterns = [
    path('doohickeys/<short_code:doohickey_id>/', views.doohickey_display),
    ...
]
```

Your view will then be handed the resulting shortcode string as an argument, for easy 
model lookup.

Additionally, a serializer field is provided for use with Django REST
Framework (it must be installed to use this feature.)

```
from rest_framework.serializers import Serializer
from short_stuff.django.serializers import ShortCodeField

class ShortCodeSerializer(Serializer):
    test_field = ShortCodeField()
```


## FAQ

> Is eight bytes enough randomness?

Yes.

> Are you sure?

If you're building something that needs more, you won't wonder. You'll know. 
And you'll have money to make it happen right. Hint: YouTube's using eight bytes.

> Ok, but a collision could happen, right? What do I do then?

Your database should prevent the row from being inserted for you. Let it fail-- the cost of adding 
complexity rather than having the user resubmit a request for a 1 in 2^34 chance of a clash 
is not worth it.

> What if I don't need UUIDs, or I'd prefer to use integers, or byte strings?

Thankfully, [Python's UUID objects](https://docs.python.org/3/library/uuid.html#uuid.UUID.bytes) have properties on 
them that allow you to retrieve their values in the forms of strings, integers, bytes, etc. In most cases, converting
to your desired format is one more line of code.

> I'd like to use a different number of bytes than the default 8 that `gen_shortcode` provides.

You can specify the number of bytes you want to use as an argument, like this:

```
>>> from short_stuff import gen_shortcode
>>> gen_shortcode(10)
'_WMWaDe4RsauOQ'
```

## Testing

To run tests, run the following from the repository root:

```
pip install -r testing_requirements.txt
pip install -e .
pytest
```

## Special Thanks

Special thanks to [KathTheDragon](https://github.com/KathTheDragon/) for helping me figure out the 
probability of collisions.

And to Amber, the love of my life, for putting up with me nerding 
out while I stepped through what this library does.
