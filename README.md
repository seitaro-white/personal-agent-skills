# Personal Agent Skills

Personal planning and review skills packaged for [Pi](https://pi.dev).

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
- `create-plan`
- `draft-plan`
- `grill-me`
- `hand-off`
- `review-changes`
- `review-plan`
- `start-worker`

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
