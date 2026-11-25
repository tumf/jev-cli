## ADDED Requirements

### Requirement: Cloudflare score descriptions
MCP SHALL explain in the score tool and in the run tool's score question description that Clef scores are probability-weighted and may be fractional, on a scale starting at zero.

#### Scenario: An MCP caller reads the score schema
- **WHEN** an MCP caller inspects the score levels description or the run question criteria description
- **THEN** both descriptions SHALL state levels are numbered from zero and scores may be fractional, for example Clef probability-weighted scores
