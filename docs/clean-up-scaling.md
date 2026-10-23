# Scaling clean-up to larger codebases

Future design note, not part of the current skill instructions. Keep cleanup direct for small repositories; introduce delegation only when repository size warrants it.

## Preferred split

Delegate inspection by coherent subsystem, with each reviewer using the same cleanup principles. Include the subsystem's related code, tests, and documentation in its scope.

Avoid splitting primarily by principle (duplication, historical residue, etc.): each reviewer may need to read much of the same repository, and related findings can become disconnected. A focused repository-wide documentation consistency review may be a useful exception.

## Proposed approach

1. **Map the repository.** A coordinator identifies coherent subsystems and shared code, then defines bounded review scopes. Share a brief repository map with reviewers.
2. **Inspect in parallel.** Area reviewers report actionable findings and suspected cross-boundary relationships. Start with review-only delegation, not concurrent editing.
3. **Reconcile globally.** The coordinator checks cross-subsystem duplication, contradictory documentation, competing conventions, and sources of truth. Reconcile findings before choosing changes; flag structural redesigns for separate work.
4. **Apply and verify.** The coordinator applies focused cleanups, or delegates clearly non-overlapping edits. Avoid concurrent changes to shared files and run relevant checks across affected subsystem boundaries.

Modularity makes area-based review practical, but does not remove the need for a global pass: many cleanup problems occur between otherwise well-separated modules.

Do not turn this into a mandatory multi-agent process. Choose scopes and delegation based on the actual repository, rather than a fixed number of agents or arbitrary directory sizes.
