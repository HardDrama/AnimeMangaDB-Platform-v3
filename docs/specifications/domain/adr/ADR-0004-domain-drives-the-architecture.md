# ADR-0004 — The Domain Drives the Architecture

## Status

Accepted

## Context

Platform v2 evolved from implementation details and accumulated compatibility constraints. Platform v3 requires a stable model that is not reshaped by database, API, provider, or frontend convenience.

## Decision

The certified Domain Specification is the source of truth for Platform v3 behavior. Implementation layers must conform to the domain. Code may not introduce or change domain behavior unless the specification and relevant ADRs define it first.

## Consequences

### Positive

- Domain behavior remains consistent across layers.
- Architectural drift becomes easier to detect.
- Future contributors can understand why behavior exists.
- Infrastructure redesigns do not redefine the platform model.

### Negative

- Domain changes require documentation before implementation.
- Some implementation shortcuts are intentionally forbidden.

## Rules established

- Domain changes require specification review.
- Major decisions require an ADR.
- Tests verify implementations against the domain contract.
- Infrastructure must not redefine identity or ownership.
