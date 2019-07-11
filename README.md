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

Still working on testing and getting this package on PyPi, but if you want to use it now,
you can install it as follows:

```
pip install -e git+https://github.com/Artconomy/short_stuff.git@0.1.0#egg=short_stuff
```

And you can add it to your local requirements.txt using a line like this:

```
-e git+https://github.com/Artconomy/short_stuff.git@0.1.0#egg=short_stuff
```

## Quick Guide

For a function which will generate a desired UUID with eight bytes worth of random data, use `gen_unique_id`.

```
>>> from short_stuff import gen_unique_id
>>> gen_unique_id()
UUID('c4e21057-6b8a-4dc0-8000-000000000000')
```

Notice that this is a truncated [UUID](https://docs.python.org/3/library/uuid.html), with everything beyond the first
eight bytes zeroed out.

Once you have an ID, you can run `slugify_uuid` on it to get your slug.

```
>>> from short_stuff import gen_unique_id, slugify
>>> slugify(gen_unique_id())
'avThRgixR_OA'
```

Need to turn your slug back into a UUID? No problem!

```
>>> from short_stuff import unslugify
>>> unslugify('avThRgixR_OA')
UUID('6af4e146-08b1-47f3-8000-000000000000')
```

## Django

If you're using a UUIDField and want to take advantage of short_stuff's shortcode generation, you'll want
to set a default on your field model.

```
from django.db import models
from short_stuff import gen_unique_id


class Doohickey(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True, default=gen_unique_id)

```

**NOTICE**: Use `gen_unique_id` and not `gen_unique_id()`! if you don't omit the parentheses, the function
will evaluate during the class definition and Django will attempt to set ALL new rows for the table with
that default.

Now that you have the shortcodes on your models, you'll want to make it possible to refer to them in your URLs.

To do this, register the provided path converter:

```
from django.urls import path, register_converter
from short_stuff import ShortUIDConverter

from . import views

register_converter(converters.ShortUIDConverter, 'short_uid')

urlpatterns = [
    path('doohickeys/<short_uid:doohickey_id>/', views.doohickey_display),
    ...
]
```

Your view will then be handed the resulting converted UUID as an argument, for easy 
model lookup.

Note that `ShortUIDConverter` will work on full length UUIDs as well, so if you've got an old 
model that has a full UUID, it can handle the resulting code, which would be something like
'Ot7-LXrERNmmlNljtGLuww'. It can, of course, also be used alongside existing routes that take
a full UUID, since Django's routing system is sophisticated enough to handle both:

```
    ...
    path('doohickeys/<uuid:doohickey_id>/', views.doohickey_display),
    path('doohickeys/<short_uid:doohickey_id>/', views.doohickey_display),
    ...
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

> I'd like to use a different number of bytes than the default 8 that `gen_unique_id` provides.

`gen_unique_id` is just a wrapper around a function called `gen_guid`, which can be given an argument of how many 
bytes you wish to use. By default, it will use the full 16 required by UUIDs. If you wanted to generate a UUID with 
only five bytes filled in, you could do:

```
>>> from short_stuff import gen_guid
>>> gen_guid(5)
UUID('ef9b315a-6600-4000-8000-000000000000')
```

## Testing

To run tests:

```
pip install -r testing_requirements.txt
pytest
```

## Special Thanks

Special thanks to [KathTheDragon](https://github.com/KathTheDragon/) for helping me figure out the 
probability of collisions.

And to Amber, the love of my life, for putting up with me nerding 
out while I stepped through what this library does.
