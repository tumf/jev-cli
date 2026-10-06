## ADDED Requirements

### Requirement: Cloudflare provider parity
The MCP server SHALL expose cloudflare as a provider and use the shared client with the effective payload model, preserving existing MCP input validation and defaults.

#### Scenario: Cloudflare MCP evaluation
- **WHEN** an MCP caller selects cloudflare and model clef or clef-flash
- **THEN** the MCP schema SHALL accept the provider and the shared endpoint SHALL match the effective model

#### Scenario: Cloudflare MCP configuration error
- **WHEN** cloudflare configuration is invalid
- **THEN** the MCP tool SHALL return a ToolError without successful output or network access
