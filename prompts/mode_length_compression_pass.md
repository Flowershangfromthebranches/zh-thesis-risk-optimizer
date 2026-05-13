# Prompt: LENGTH_COMPRESSION_PASS

Use this prompt when the revised draft exceeds the allowed length budget, such as a 17000-character thesis expanding to about 24000 characters.

## Input

- Original text.
- Current expanded draft.
- Maximum allowed growth.
- Protected list.

## Output

### 1. Over-Expansion Diagnosis

- Original chars:
- Current chars:
- Allowed delta:
- Current delta:
- Status:

### 2. Sections With Excessive Growth

| section | original_chars | current_chars | delta | compress_priority |
|---|---:|---:|---:|---|

### 3. Compressible Additions

- New broad background.
- Repeated significance sentences.
- Generic value judgments.
- Repeated module explanation.
- Mechanical connector structures.

### 4. Protected Non-Compressible Content

- Test data.
- Technical objects.
- Citations.
- Conclusions.
- Parameters.
- Paths, code, interfaces, Payload, and formulas.

### 5. Compressed Revision

Only output compressed sections or paragraphs.

### 6. New Length Budget Table

| section | before_chars | after_chars | delta | budget | status |
|---|---:|---:|---:|---:|---|

## Compression Priority

1. Delete newly added macro background.
2. Delete repeated significance claims.
3. Delete generic value judgments.
4. Merge repeated module explanations.
5. Compress "first-second-additionally" structures.
6. Preserve test data, technical objects, citations, and conclusions.

## Safety

Do not compress by deleting necessary citations, data, parameters, paths, code, or conclusions.
