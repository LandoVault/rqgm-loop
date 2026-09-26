# `slug.slugify` — specification
`slugify(text: str) -> str`
1. Lowercase the text.
2. Replace every run of characters that are not a-z or 0-9 with a single hyphen.
3. Remove leading and trailing hyphens.
Interface (must not change): module `slug`, function `slugify(text)`.
