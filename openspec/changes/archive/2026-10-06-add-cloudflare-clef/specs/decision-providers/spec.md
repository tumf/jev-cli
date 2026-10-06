## ADDED Requirements

### Requirement: Cloudflare decision model provider
The client SHALL support provider cloudflare with default model clef-flash and explicit model clef, using the existing state/questions contract and without changing other providers.

#### Scenario: Evaluate with either model
- **WHEN** cloudflare is selected with clef or clef-flash and a valid account ID and token
- **THEN** the shared client SHALL POST the same selected model in the body to the corresponding Workers AI model URL using Bearer authentication

#### Scenario: Invalid configuration
- **WHEN** account ID is absent or not 32 hexadecimal characters, or the selected cloudflare model is unsupported
- **THEN** the client SHALL report a structured configuration error before network access, allowing an explicit endpoint override to replace the account-derived URL only

### Requirement: Cloudflare normalized decisions
The client SHALL unwrap successful Cloudflare REST envelopes, remove answer type discriminators and preserve decision probabilities, weighted score, confidence, legend, model and usage without synthesizing values.

#### Scenario: Successful typed decisions
- **WHEN** Workers AI returns a successful envelope with noul, choice and score answers
- **THEN** normal JSON and --value output SHALL expose the actual decisions through the existing answer keys

#### Scenario: Failed envelope
- **WHEN** an envelope reports failure or lacks an object result or object answers
- **THEN** the client SHALL fail and SHALL NOT emit successful decisions

### Requirement: Cloudflare credential and request isolation
The client SHALL use CLOUDFLARE_API_TOKEN or the cloudflare credential-store entry independently of other providers, and SHALL preserve additional run fields.

#### Scenario: Authentication setup and batched request
- **WHEN** the user stores a cloudflare token and submits a complete request with images
- **THEN** other stored tokens SHALL remain unchanged and the images field SHALL pass through unchanged
