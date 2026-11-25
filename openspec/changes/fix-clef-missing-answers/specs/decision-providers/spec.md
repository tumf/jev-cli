## ADDED Requirements

### Requirement: Cloudflare decision response completeness
The shared Cloudflare client SHALL reject a successful REST envelope that omits any submitted question ID from its answers. This check SHALL NOT change other providers or alter existing valid scores or probabilities.

#### Scenario: A requested answer is missing
- **WHEN** a Cloudflare response omits any requested question ID
- **THEN** the CLI SHALL fail without decision output and MCP SHALL return a tool error rather than a successful decision result

#### Scenario: All requested answers are present
- **WHEN** Cloudflare supplies an answer for each requested question ID
- **THEN** normalized decisions SHALL preserve the returned values, including zero and fractional scores
