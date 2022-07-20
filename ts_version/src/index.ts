import { v4 as uuidv4, parse as uuidParse } from 'uuid';

/*Pads a sequence of raw bytes to make them the required size of a UUID.
Note that if you're using an int as your source for instantiating a UUID,
you should not use this function. Just use UUID(your_int_here).
*/
export function padGuidBytes(rawBytes: Uint8Array): Uint8Array {
  if (rawBytes.length > 16 || rawBytes.length < 1) {
    throw new Error('Byte length must be between 1 and 16.');
  }
  return Uint8Array.from([...rawBytes, ...Array(16 - rawBytes.length).fill(0)])
}

/*Takes a UUID and turns it into a URLencode compatible base64 slug.*/
export function slugify(uid: string): string {

  const byteArray = [...uuidParse(uid) as Uint8Array];
  while (byteArray[byteArray.length - 1] === 0) { // While the last element is a 0,
    byteArray.pop();                  // Remove that last element
  }

  let str = btoa(String.fromCharCode.apply(null, byteArray));
  str = str.replace(/\+/g, "-").replace(/\//g, "_").trim().replace(/=*$/g, '')
  return str
}

/*Note: This will only ever add up to two '='s unless the source string is corrupt.
https://stackoverflow.com/questions/1228701/code-for-decoding-encoding-a-modified-base64-url*/
function padEncodedSlug(slug: string): string {
  return slug + ("=".repeat(slug.length % 4))
}

/*Takes a URLencode compatible base64 slug and turns it into a UUID, padding the end if needed.*/
export function unSlugify(slug: string): string {
  let paddedSlug = padEncodedSlug(slug)
  paddedSlug = paddedSlug.replace(/-/g, "+").replace(/_/g, "/").trim();
  const binary = atob(paddedSlug).split("")

  const rawString = new Uint8Array(binary.map(function(c) {
    return c.charCodeAt(0);
  }));
  const rawBytes = padGuidBytes(rawString)
  if (rawBytes.length > 16) {
    throw new Error('Too many bytes for a UUID');
  }
  return uuidv4({ random: rawBytes })
}


/*Generates a UUID that is truncated to a certain number of bytes and padded afterward.*/
export function genShortcodeUuid(byteLength = 16): string {
  if (byteLength > 16 || byteLength < 1) {
    throw new Error('Byte length must be between 1 and 16.');
  }
  let byteArray = Uint8Array.from({ length: byteLength }, () => Math.floor(Math.random() * 255));
  byteArray = padGuidBytes(byteArray)
  return uuidv4({ random: byteArray })
}

export function genShortcode(byteLength = 8): string {
  return slugify(genShortcodeUuid(byteLength))
}
