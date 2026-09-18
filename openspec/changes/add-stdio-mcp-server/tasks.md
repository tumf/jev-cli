## Implementation Tasks

- [ ] Add the official Python MCP SDK version 2.x as a normal dependency and register the `jev-mcp` console command without an optional package extra. Remove the dependency-free claim from every package, module, and documentation occurrence and synchronize `uv.lock`. (verification: integration - `make test`; verification-id: mcp-server-tests)
- [ ] Implement a stdio-only MCP adapter exposing `noul`, `choice`, `score`, and `run`, reusing the existing provider, credential, request, and response code directly rather than invoking the CLI as a subprocess. Validate tool inputs before network access and keep stdout exclusive to MCP protocol traffic. (verification: integration - `make test`; verification-id: mcp-server-tests)
- [ ] Add mocked tests that discover and call all four tools through the MCP SDK transport, verify payload/provider/model/endpoint forwarding and structured responses, and cover invalid choice options, score levels, run payloads, invalid `JEV_PROVIDER`, propagated `CliError`, clean stdio framing, and verbatim `-` and `@path` state strings without stdin or file access. Preserve all existing CLI tests. (verification: integration - `make test`; verification-id: mcp-server-tests)
- [ ] Update README and the source Agent Skill, then regenerate the bundled skill copy, documenting the single normal install command, `jev-mcp`, authentication reuse, four tools, and a minimal stdio MCP client configuration. (verification: integration - `make test`; verification-id: mcp-server-tests)

## Final Validation

Archive validation is the authoritative final OpenSpec gate. Expected archive gate: `cflx openspec validate add-stdio-mcp-server --archive-gate`.
