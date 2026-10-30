# gke-api-docs-copilot

Grounded API documentation copilot: answers questions about OpenAPI specs with citations (operation ID, path, spec version). Self-hosted vLLM on an ephemeral GKE cluster, Cloud SQL pgvector.

**Status:** design stage (no application code yet).

- Architecture and design: [docs/design.md](docs/design.md) (diagram: [docs/architecture.png](docs/architecture.png), editable source `docs/architecture.drawio`); CI: [docs/ci-design.md](docs/ci-design.md)
- **Teardown constraint:** everything on GCP that costs money must be deleted at session end; teardown must never hang or fail silently.

## Run manually

TBD, filled after implementation.
