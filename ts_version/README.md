# Short Stuff

**Typescript port of [short_stuff](https://github.com/Artconomy/short_stuff) built in python.**

ShortStuff is a set of helper functions used for generating short unique
identifiers, such as those used in YouTube video IDs or in URL shorteners.

ShortStuff does this by generating random byte strings, running them through
base64 encoding and then doing some cleanup for compatibility.

Most distinct about the methodology is that it piggy-backs on UUIDs. That means
that if you want to leverage your database or library's native UUID support,
you can do so, and helper functions are provided for this.

---

## Installation

Short Stuff has been tested on node 16 and 17.

To install:

```
npm install shortStuff
```

## Quick Guide

To generate a short code:

```javascript
import { genShortcode } from 'shortStuff'
console.log(genShortcode())
> 'XtFxMb7qTJ-A'
```

To turn this code into a UUID (such as for DB storage):

```javascript
import { unSlugify } from 'shortStuff'
console.log(unSlugify('XtFxMb7qTJ-A'))
> '5ed17131-beea-4c9f-8000-000000000000'
```

Notice that this is a truncated [uuid](https://github.com/uuidjs/uuid), with
everything beyond the first eight bytes zeroed out.

To turn the UUID back into a slug:

```javascript
import { slugify } from 'shortStuff'
console.log(slugify('5ed17131-beea-4c9f-8000-000000000000'))
> 'XtFxMb7qTJ-A'
```
