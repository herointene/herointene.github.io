"""Rebuild the preserved original source, keeping cat-beta unpublished."""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory

from check_site import check


SOURCE_REF = "cc90dfb7f016473eae2f4a2ff17bbdb10d19ecff"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    parser.add_argument("--report", type=Path, default=Path("test-results/site-checks.json"))
    args = parser.parse_args()
    if args.site_dir.exists():
        parser.error(f"Output already exists; choose a new directory: {args.site_dir}")
    with TemporaryDirectory(prefix="ting-rollback-") as directory:
        original = Path(directory)
        archive = subprocess.check_output(["git", "archive", "--format=tar", SOURCE_REF])
        with tarfile.open(fileobj=io.BytesIO(archive)) as source:
            source.extractall(original, filter="data")
        config = original / "mkdocs.yml"
        text = config.read_text(encoding="utf-8")
        assert "exclude_docs:" not in text, "Rollback source changed unexpectedly"
        # These two compatibility edits retain the original appearance and prevent
        # a rollback from republishing the draft. Original Git objects stay intact.
        text = text.replace("materialx.emoji.", "material.extensions.emoji.")
        config.write_text(text + "\nexclude_docs: |\n  /talk/cat-beta.md\n", encoding="utf-8")
        subprocess.run([sys.executable, "-m", "mkdocs", "build", "--clean", "--strict", "-f", str(config)],
                       cwd=original, check=True)
        report = check(original / "site", original / "docs")
        report["rollback_source_ref"] = SOURCE_REF
        args.site_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(original / "site", args.site_dir)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
