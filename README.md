# Plone Monorepo Helper

[![QA](https://github.com/kitconcept/plone-repo-helper/actions/workflows/qa.yml/badge.svg)](https://github.com/kitconcept/plone-repo-helper/actions/workflows/qa.yml)
[![Tests](https://github.com/kitconcept/plone-repo-helper/actions/workflows/test.yml/badge.svg)](https://github.com/kitconcept/plone-repo-helper/actions/workflows/test.yml)

## Overview

The **Plone Monorepo Helper** is a tool designed to manage monorepos containing a `repository.toml` configuration file at the repository root. It provides various commands to streamline repository management, versioning, and release processes.

## Setup

Ensure that your monorepo contains a `repository.toml` file. Below is an example of such a configuration:

```toml
[repository]
name = "fake-distribution"
managed_by_uv = true
changelog = "CHANGELOG.md"
version = "version.txt"
compose = "docker-compose.yml"

[backend]
path = "backend"

[backend.package]
name = "fake.distribution"
path = "backend"
changelog = "backend/CHANGELOG.md"
towncrier_settings = "backend/pyproject.toml"

[frontend]
path = "frontend"

[frontend.package]
name = "fake-distribution"
path = "frontend/packages/fake-distribution"
changelog = "frontend/packages/fake-distribution/CHANGELOG.md"
towncrier_settings = "frontend/packages/fake-distribution/towncrier.toml"
```

## Usage

### List Available Commands
To see all available commands, run:

```bash
uv run repo_helper
```

### Check Installed Version
To check the installed version of the tool, use:

```bash
uv run repo_helper --version
```

## Check repository versions

List current versions for:

- Repository
- Backend package
- Frontend package

```bash
uv run repo_helper version
```

## Releasing Monorepo Packages

The release process consists of two subcommands:
- **`changelog`** – Generates a draft changelog for review.
- **`do`** – Performs the package release.

### Generate Changelog
To generate and display the draft changelog, run:

```bash
uv run repo_helper release changelog
```

### Perform Release
The `do` command creates a new release and accepts the following arguments:

#### `version`
The version argument defines the new version to be used in the release. It can be a specific version number or a version segment. Below is a reference table showing how version segments modify an existing `1.0.0` version:

| Segment | New Version |
|---------|------------|
| `release` | `1.0.0` |
| `major` | `2.0.0` |
| `minor` | `1.1.0` |
| `micro` / `patch` / `fix` | `1.0.1` |
| `a` / `alpha` | `1.0.0a0` |
| `b` / `beta` | `1.0.0b0` |
| `c` / `rc` / `pre` / `preview` | `1.0.0rc0` |
| `r` / `rev` / `post` | `1.0.0.post0` |
| `dev` | `1.0.0.dev0` |

#### `--dry-run`
Use this flag to simulate the release process without actually publishing the new version.

**Example:**

```bash
uv run repo_helper release do a
```

This will create an `alpha` release.

---

## Plone Distribution Support

The following commands are available exclusively for distributions based on `Products.CMFPlone`.

### Check Plone Version
To check the current Plone version, run:

```bash
uv run repo_helper plone check
```

### Upgrade Plone
To upgrade Plone to a specific version, use:

```bash
uv run repo_helper plone upgrade 6.1.1
```
