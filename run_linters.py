"""Helper to run pylint, bandit, and flake8 and write reports to files.

This script uses the current Python executable to invoke each tool and
captures stdout/stderr to files in the repository root.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

commands = [
    (sys.executable, ["-m", "pylint", "inventory_system.py"], ROOT / "pylint_report.txt"),
    (sys.executable, ["-m", "bandit", "-r", "inventory_system.py"], ROOT / "bandit_report.txt"),
    (sys.executable, ["-m", "flake8", "inventory_system.py"], ROOT / "flake8_report.txt"),
]

def run_and_save(cmd_exe, args, outfile: Path):
    print(f"Running: {cmd_exe} {' '.join(args)} -> {outfile.name}")
    try:
        proc = subprocess.run([cmd_exe] + args, capture_output=True, text=True, check=False, cwd=ROOT)
        content = "".join([proc.stdout or "", proc.stderr or ""])
        outfile.write_text(content, encoding="utf-8")
    except Exception as exc:
        print(f"Failed to run {' '.join(args)}: {exc}")


def main():
    for exe, args, out in commands:
        run_and_save(exe, args, out)
    print("Reports written: pylint_report.txt bandit_report.txt flake8_report.txt")


if __name__ == "__main__":
    main()
