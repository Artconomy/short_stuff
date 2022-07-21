import { v4 as uuidv4 } from 'uuid';
import { genShortcodeUuid, padGuidBytes, slugify, unSlugify } from ".";

test("e2e base", () => {
  for (let index = 0; index < 100; index++) {
    const thing = uuidv4();
    expect(unSlugify(slugify(thing))).toBe(thing);
  }
});

test("e2e shorthand", () => {
  for (let index = 0; index < 100; index++) {
    const thing = genShortcodeUuid();
    expect(unSlugify(slugify(thing))).toBe(thing);
  }
});

test("pad guid bytes should throw if 0 bytes", () => {
  expect(() => padGuidBytes(new Uint8Array([]))).toThrow(Error);
});

test("gen guid limit should throw if 0", () => {
  expect(() => genShortcodeUuid(0)).toThrow(Error);
});
