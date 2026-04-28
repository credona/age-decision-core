import json
import os
import subprocess
from pathlib import Path

PROJECT_FILE = Path("project.json")


def run(command: list[str]) -> str:
    result = subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def main() -> None:
    metadata = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
    version = metadata["version"]
    tag = f"v{version}"

    if os.getenv("GITHUB_REF_NAME") != "main":
        print("Automatic tagging skipped because this is not main.")
        return

    existing_tags = run(["git", "tag", "--list", tag])
    if existing_tags:
        print(f"Tag already exists locally: {tag}")
        return

    remote_tag = subprocess.run(
        ["git", "ls-remote", "--tags", "origin", f"refs/tags/{tag}"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()

    if remote_tag:
        print(f"Tag already exists remotely: {tag}")
        return

    token = os.getenv("AGE_DECISION_RELEASE_TOKEN")
    repository = os.getenv("GITHUB_REPOSITORY")

    if token and repository:
        run(
            [
                "git",
                "remote",
                "set-url",
                "origin",
                f"https://x-access-token:{token}@github.com/{repository}.git",
            ]
        )

    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    run(["git", "tag", "-a", tag, "-m", f"Release {tag}"])
    run(["git", "push", "origin", tag])

    print(f"Created and pushed tag: {tag}")


if __name__ == "__main__":
    main()
