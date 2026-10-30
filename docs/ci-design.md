# CI design

Written before `.github/workflows/ci.yml`; the workflow implements exactly this.

## Principles
- Keyless: no GCP credentials, no secrets, no OIDC federation. CI never touches GCP.
- `permissions: contents: read` only.
- Triggers: `pull_request` (every PR, no path/branch filters) and `push` to `main`.
- Two jobs, id and `name` exactly `lint` and `test` (no matrix), because branch protection requires status checks named `lint` and `test`.

## Job `lint`
1. `ruff check .` and `ruff format --check .` via `uv run --no-project --with ruff`.
2. `shellcheck scripts/*.sh` (skips cleanly if there are no `.sh` files yet).

## Job `test`
1. `python -m unittest discover -s tests -v` (stdlib only; Python 3.12 via uv).
2. `kubeconform -strict -summary -ignore-missing-schemas` on `k8s/`; skipped with a message if the dir is missing or has no YAML.
3. Kyverno policy check: not run here. Policies live in the platform repo (`gke-ai-observer`, `check-policies.sh`, kyverno CLI 1.19.1). Manifests added later get checked in that repo's CI.

## Pinning
- Actions pinned to commit SHAs, resolved via the GitHub API (tag -> commit): `actions/checkout` v7.0.1 = `3d3c42e5...`, `astral-sh/setup-uv` v10.3.3 = `68559e99...`. Full SHAs are in the workflow comments/uses lines.
- `shellcheck` v0.11.0 and `kubeconform` v0.8.0 downloaded from their GitHub releases and verified against a pinned sha256. The hashes were computed from a download made while authoring (not from an upstream-published checksum file), so they pin integrity going forward but were not independently cross-checked.
- ruff is not version-pinned (`--with ruff` resolves latest). Known gap; pin once a version is chosen in implementation.

## Secret scanning
`betterleaks` is Miguel's tool. **Mandatory local step before every push/PR:**

```
betterleaks dir .
```
(bare `betterleaks .` errors). CI does not run it: it is keyless and no safe pinned install was verified, so none is invented here.

## Required status checks
`lint` and `test`, strict (branch must be up to date), plus 1 approving review on `main`.
