# coding=utf-8
# Copyright (C) 2019 Larry Wang <larry.wang.801@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from pathlib import Path
import buildVars
import subprocess


def _run(command: list[str], *, check: bool=True) -> None:
	_ = subprocess.run(command, check=check, text=True, capture_output=True)


def _succeeds(command: list[str]) -> bool:
	return subprocess.run(command, check=False, text=True, capture_output=True).returncode == 0


name = buildVars.addon_info["addon_name"]
version = buildVars.addon_info["addon_version"]
asset = str(Path(f"{name}-{version}.nvda-addon"))

# Refresh local tag references from remote before checking for existing tag.
_run(["git", "fetch", "--tags"], check=False)

# Reuse existing tag if present.
tag_exists = _succeeds(["git", "rev-parse", "-q", "--verify", f"refs/tags/{version}"])
if not tag_exists:
	_run(["git", "tag", "-m", version, version])

# Push current tag; this is harmless if already present remotely.
_run(["git", "push", "origin", f"refs/tags/{version}"], check=False)

release_exists = _succeeds(["gh", "release", "view", version])
if release_exists:
	# Update notes and overwrite the asset when the release already exists.
	_run(["gh", "release", "edit", version, "--generate-notes"], check=False)
	_run(["gh", "release", "upload", version, asset, "--clobber"])
else:
	_run(["gh", "release", "create", version, "--generate-notes", asset])
