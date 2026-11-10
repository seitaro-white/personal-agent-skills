"""Write a role file's prompt body to a file and print the Pi launch arguments, NUL-separated.

A role file is markdown with `key: value` frontmatter (`model`, `thinking`)
and the role's system prompt as its body. The body, without frontmatter, is
written to <prompt-file>, which Pi reads via --append-system-prompt.

Usage: python3 role_launch_args.py <role-file> <prompt-file>
"""

import sys
from pathlib import Path


def read_role(role_path: Path) -> tuple[dict[str, str], str]:
    """Split a role file into its frontmatter fields and prompt body."""
    _, frontmatter, body = role_path.read_text().split("---\n", 2)
    fields = dict(
        line.split(":", 1) for line in frontmatter.splitlines() if ":" in line
    )
    return {key.strip(): value.strip() for key, value in fields.items()}, body.strip()


def build_launch_args(fields: dict[str, str], prompt_path: str) -> list[str]:
    """Turn role fields and a prompt file path into Pi CLI arguments."""
    model_and_thinking_args = []
    if "model" in fields:
        model_and_thinking_args += ["--model", fields["model"]]
    if "thinking" in fields:
        model_and_thinking_args += ["--thinking", fields["thinking"]]
    return [*model_and_thinking_args, "--append-system-prompt", prompt_path]


if __name__ == "__main__":
    fields, prompt = read_role(Path(sys.argv[1]))
    prompt_path = Path(sys.argv[2])
    prompt_path.write_text(prompt)
    sys.stdout.write("\0".join(build_launch_args(fields, str(prompt_path))) + "\0")
