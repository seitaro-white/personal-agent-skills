"""Regression tests for agent launches and handoff, without starting live agents."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "roles"))
from role_launch_args import build_launch_args, read_role

SCRIPTS = ("start-worker/start-worker.sh", "hand-off/hand-off.sh")


def pi_launch_args(calls):
    """Return the Pi arguments from the recorded agent launch."""
    start = next(call for call in calls if call[:2] == ["agent", "start"])
    return start[start.index("--") + 1:]


def role_launch_args(script, prompt_path):
    """Return the model, thinking and prompt arguments from a launch script's role file."""
    role = "worker" if script.startswith("start-worker/") else "orchestrator"
    fields, _ = read_role(ROOT / "roles" / f"{role}.md")
    return build_launch_args(fields, prompt_path)


class RoleLaunchArgsTests(unittest.TestCase):
    def test_role_file_becomes_model_thinking_and_prompt_without_frontmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            role_path = Path(directory) / "role.md"
            role_path.write_text("---\nname: worker\nmodel: provider/model-id\nthinking: high\n---\n\n## Role\n\nDo the task.\n")
            prompt_path = Path(directory) / "prompt.txt"
            result = subprocess.run(
                [sys.executable, str(ROOT / "roles" / "role_launch_args.py"), str(role_path), str(prompt_path)],
                capture_output=True, text=True, check=True,
            )
            self.assertEqual(
                result.stdout.split("\0")[:-1],
                ["--model", "provider/model-id", "--thinking", "high", "--append-system-prompt", str(prompt_path)],
            )
            self.assertEqual(prompt_path.read_text(), "## Role\n\nDo the task.")


class AgentHandoffTests(unittest.TestCase):
    def run_handoff(self, script, *, failure="", existing=False, profiles_set=False, profile_args=None):
        """Run a launch script against a recording Herdr stub."""
        with tempfile.TemporaryDirectory() as directory:
            cwd = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            task = cwd / "task.md"
            task.write_text("Implement the task.")
            log = cwd / "calls.jsonl"
            herdr = cwd / "herdr"
            herdr.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "args = sys.argv[1:]\n"
                "with open(os.environ['CALL_LOG'], 'a') as log:\n"
                "    log.write(json.dumps(args) + '\\n')\n"
                "if args[:2] == ['agent', 'get']:\n"
                "    sys.exit(0 if os.environ['EXISTING'] == '1' else 1)\n"
                "if args[:2] == ['agent', os.environ['FAILURE']]:\n"
                "    print('simulated handoff failure', file=sys.stderr)\n"
                "    sys.exit(1)\n"
                "print(json.dumps({'result': {\n"
                "    'workspace': {'workspace_id': 'w2'},\n"
                "    'tab': {'tab_id': 'w2:t1'},\n"
                "    'root_pane': {'pane_id': 'w2:p1'}}}))\n"
            )
            herdr.chmod(0o755)
            args = [str(task)]
            if script.startswith("start-worker/"):
                args.insert(0, "feature")
            env = dict(os.environ)
            env.pop("PI_AGENT_PROFILES", None)
            if profiles_set:
                profiles = cwd / "launch profiles"
                profiles.mkdir()
                env["PI_AGENT_PROFILES"] = str(profiles)
                if profile_args is not None:
                    role = "worker" if script.startswith("start-worker/") else "orchestrator"
                    (profiles / f"{role}.args").write_text("\n".join(profile_args) + "\n")
            result = subprocess.run(
                ["bash", str(ROOT / "skills" / script), *args],
                cwd=cwd,
                env={
                    **env,
                    "PATH": f"{cwd}:{os.environ['PATH']}",
                    "HERDR_WORKSPACE_ID": "w1",
                    "CALL_LOG": str(log),
                    "FAILURE": failure,
                    "EXISTING": "1" if existing else "0",
                },
                text=True,
                capture_output=True,
                check=False,
                timeout=10,
            )
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            if any(call[:2] == ["agent", "start"] for call in calls):
                launch_args = pi_launch_args(calls)
                self.assertTrue(all("\n" not in arg for arg in launch_args))
                prompt_path = Path(launch_args[launch_args.index("--append-system-prompt") + 1])
                self.addCleanup(prompt_path.unlink)
                role = "worker" if script.startswith("start-worker/") else "orchestrator"
                _, prompt = read_role(ROOT / "roles" / f"{role}.md")
                self.assertEqual(prompt_path.read_text(), prompt)
            return result, calls

    def test_launch_profile_arguments_precede_role_arguments_in_file_order(self):
        profile_args = ["--provider", "test-provider", "-e", "/extensions/path with spaces/index.js"]
        for script in SCRIPTS:
            with self.subTest(script=script):
                result, calls = self.run_handoff(script, profiles_set=True, profile_args=profile_args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    pi_launch_args(calls),
                    [*profile_args, *role_launch_args(script, pi_launch_args(calls)[-1])],
                )

    def test_missing_launch_profile_works_under_nounset_with_only_role_arguments(self):
        for script in SCRIPTS:
            for profiles_set in (False, True):
                with self.subTest(script=script, profiles_set=profiles_set):
                    result, calls = self.run_handoff(script, profiles_set=profiles_set)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(
                        pi_launch_args(calls),
                        role_launch_args(script, pi_launch_args(calls)[-1]),
                    )

    def test_waits_for_readiness_and_confirms_working_before_reporting_success(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                result, calls = self.run_handoff(script)
                self.assertEqual(result.returncode, 0, result.stderr)
                start = next(i for i, call in enumerate(calls) if call[:2] == ["agent", "start"])
                wait = next(i for i, call in enumerate(calls) if call[:2] == ["agent", "wait"])
                prompt = next(i for i, call in enumerate(calls) if call[:2] == ["agent", "prompt"])
                self.assertLess(start, wait)
                self.assertLess(wait, prompt)
                self.assertIn("idle", calls[wait])
                self.assertEqual(calls[wait][-2:], ["--timeout", "30000"])
                self.assertEqual(calls[prompt][-5:], ["--wait", "--until", "working", "--timeout", "30000"])
                self.assertEqual(calls[wait][2], calls[prompt][2])
                self.assertEqual(result.stdout, calls[prompt][2] + "\n")
                self.assertIn("Implement the task.", calls[prompt][3])

    def test_readiness_failure_does_not_send_task_or_report_success(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                result, calls = self.run_handoff(script, failure="wait")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("simulated handoff failure", result.stderr)
                self.assertFalse(any(call[:2] == ["agent", "prompt"] for call in calls))

    def test_pickup_failure_is_visible_and_does_not_retry_or_report_success(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                result, calls = self.run_handoff(script, failure="prompt")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("simulated handoff failure", result.stderr)
                self.assertEqual(sum(call[:2] == ["agent", "prompt"] for call in calls), 1)

    def test_existing_orchestrator_also_waits_for_readiness_and_pickup(self):
        result, calls = self.run_handoff("hand-off/hand-off.sh", existing=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any(call[:2] == ["agent", "start"] for call in calls))
        self.assertEqual([call[1] for call in calls], ["get", "wait", "prompt"])
        self.assertIn("done", calls[1])
        self.assertIn("--wait", calls[2])
        self.assertIn("working", calls[2])


if __name__ == "__main__":
    unittest.main()
