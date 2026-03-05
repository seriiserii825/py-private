# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal CLI tool for managing WordPress/web hosting projects across multiple VPS servers. Provides SSH connections, file sync, backups, and project metadata management via interactive terminal menus.

## Commands

**Run the tool:**
```sh
uv run main.py
```

**Linting & type checking:**
```sh
uv run flake8 .
uv run mypy .
uv run autopep8 --in-place --recursive .
```

**Manage dependencies:**
```sh
uv add <package>
uv remove <package>
```

## Data Files

The two core data stores are CSV files, encrypted at rest with GPG:
- `list.csv` / `list.csv.gpg` — project registry: `project_name,vps_server_name,remote_path`
- `servers.csv` / `servers.csv.gpg` — server inventory: `server_name,login_user,ip_address,password,ssh_port`

Both plain-text CSVs are git-ignored; only the `.gpg` versions are committed.

## Architecture

**Entry point**: `main.py` — interactive numbered menu dispatching to module functions.

**Modules** (`modules/`): Each file is a self-contained feature:
- `server.py` / `connectToProject.py` — SSH via `sshpass`; project/server selected with FZF
- `uploadFiles.py` — `watchdog` file watcher → rsync on change, SSH `rm` on delete
- `downloadFiles.py` — reads path from clipboard, resolves project/server, downloads via SCP
- `backups.py` — WordPress backup management via rsync
- `Projects.py` — `Project` dataclass wrapping CSV row access
- `viewProjects.py`, `findProject.py` — Rich table display + FZF search

**Utils** (`utils/`, `libs/`): Shared helpers for CSV parsing (`getProjectsFromCsv.py`), FZF selection (`selectWithFzf.py`), clipboard (`buffer.py`), and Rich printing (`classes/utils/Print.py`).

**Data flow (typical feature):**
1. User picks option in `main.py`
2. Module queries `list.csv` for project → resolves server from `servers.csv`
3. Runs SSH/rsync/SCP command via `os.system()` or `subprocess`
4. Shows result with Rich; sends `notify-send` desktop notification

## Key Conventions

- Package manager is **UV** (not pip/poetry). Always use `uv add`/`uv run`.
- SSH uses `sshpass` (password auth), not key-based auth.
- FZF is used for interactive selection throughout (`pyfzf` + `selectWithFzf.py`).
- CSV is parsed manually with no ORM — linear scans are intentional for this scale.
- `os.system()` is used alongside `subprocess` — both patterns exist in the codebase.
