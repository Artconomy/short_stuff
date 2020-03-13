import os
from uuid import UUID
from base64 import encodebytes, decodebytes


__all__ = (
    'pad_guid_bytes', 'pad_encoded_slug', 'slugify', 'unslugify', 'gen_guid',
    'gen_unique_id', 'gen_shortcode',
)


def pad_guid_bytes(raw_bytes: bytes) -> bytes:
    """Pads a sequence of raw bytes to make them the required size of a UUID."""
    if not (0 < len(raw_bytes) <= 16):
        raise ValueError("Byte length must be between 1 and 16.")
    return raw_bytes + (b'\x00' * (16 - len(raw_bytes)))


def pad_encoded_slug(slug: str) -> str:
    """Encodes a base64 string on the right with '='s."""
    # Note: This will only ever add up to two '='s unless the source string is corrupt.
    # https://stackoverflow.com/questions/1228701/code-for-decoding-encoding-a-modified-base64-url
    return slug + ("=" * (len(slug) % 4))


def slugify(uid: UUID) -> str:
    """Takes a UUID and turns it into a URLencode compatible base64 slug."""
    byte_string = uid.bytes.rstrip(b'\x00')
    byte_string = encodebytes(byte_string)
    # The encoder will add a newline on the end. We need to strip that. After said stripping, to ensure compatibility
    # with URL values, we want to swap out + and / for - and _, respectively. These are 'standard' characters that
    # can be expected from most base64 implementations, including Python's. Consult RFC4648 for full details.
    # Additionally, since the = is padding, we can remove it and restore it later when reversing the process.
    byte_string = byte_string.replace(b'+', b'-').replace(b'/', b'_').strip().rstrip(b'=')
    return byte_string.strip().decode('utf-8')


def unslugify(slug: str) -> UUID:
    """Takes a URLencode compatible base64 slug and turns it into a UUID, padding the end if needed."""
    slug = pad_encoded_slug(slug)
    byte_string = slug.encode('utf-8').replace(b'-', b'+').replace(b'_', b'/')
    raw_bytes = decodebytes(byte_string)
    if len(raw_bytes) > 16:
        raise ValueError("Too many bytes for a UUID.")
    # Pad the value, so we can have truncated UUIDs.
    raw_bytes = pad_guid_bytes(raw_bytes)
    return UUID(bytes=raw_bytes, version=4)


def gen_guid(byte_length: int = 16) -> UUID:
    """Generates a UUID that is truncated to a certain number of bytes and padded afterward."""
    if not (0 < byte_length <= 16):
        raise ValueError("Byte length must be between 1 and 16.")
    return UUID(bytes=pad_guid_bytes(os.urandom(byte_length)), version=4)


def gen_unique_id() -> UUID:
    """Returns a string of URL-compatible characters that represent 8 bytes of random information.
    This should make collisions on a single platform negligible. You can use this as the 'default' argument on,
    for instance, your Django UUID primary key field. Remember NOT to make it:

    default=gen_unique_id()

    ...but rather:

    default=gen_unique_id

    ...since it will be a static value in the first case for ALL entries instead of a new value each time.
    """
    return gen_guid(byte_length=8)

def gen_shortcode() -> str:
    return slugify(gen_unique_id())
