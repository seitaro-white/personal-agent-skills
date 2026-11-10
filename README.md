# Personal Agent Skills

Personal planning, review and agent workflow skills packaged for [Pi](https://pi.dev).

## Install in Pi

With Pi installed, run:

```bash
pi install git:github.com/seitaro-white/personal-agent-skills
```

This installs the skills for your user account (recorded in `~/.pi/agent/settings.json`). Restart Pi to load them.

To install only for the current project instead:

```bash
pi install git:github.com/seitaro-white/personal-agent-skills --local
```

Project installs are recorded in `.pi/settings.json` and load after you trust the project.

### Use a local checkout

From this repository's root, install the checkout directly:

```bash
pi install "$PWD"
```

Pi loads local packages in place without copying them, so this is useful when editing the skills.

## Included skills

- `clean-up`
- `grill-me`
- `hand-off`
- `plan`
- `review-changes`
- `start-worker`
- `write-code`

## Included subagents

Loaded by [pi-subagents](https://github.com/nicobailon/pi-subagents) from `agents/`. Workers run them on their changes before user review.

- `readability-reviewer`: renames vague identifiers and flattens nested logic, without changing behaviour. Edits files.
- `quality-reviewer`: checks correctness, bugs, duplication and unneeded complexity. Read-only; returns findings.

Each sets its model in its frontmatter. Override one per machine with `subagents.agentOverrides.<name>.model` in Pi settings.

## Roles

`roles/` holds the two long-running Herdr agents, in the same frontmatter-and-prompt format as the subagents:

- `orchestrator`: started by `hand-off`. Splits briefs into branches, starts and answers workers, and opens pull requests.
- `worker`: started by `start-worker`. Implements one branch in its own worktree and runs both reviewer subagents.

The launch scripts read `model` and `thinking` from the frontmatter and pass the body through a temporary prompt file in `/tmp` (left in place for Pi to read at startup). Machine-specific arguments, such as extension paths, come from `$PI_AGENT_PROFILES/<role>.args`.

## Manage the installation

```bash
# List configured packages
pi list

# Update the Git installation
pi update git:github.com/seitaro-white/personal-agent-skills

# Remove the Git installation
pi remove git:github.com/seitaro-white/personal-agent-skills
```

For a project-local installation, add `--local` when removing it. For a local checkout, use its absolute path instead of the Git source.
