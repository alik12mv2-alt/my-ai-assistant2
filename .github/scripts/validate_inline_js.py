#!/usr/bin/env python3
"""Syntax-check inline JavaScript in the storefront using Node.js."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
import sys

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.current = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "script":
            self.in_script = True
            self.current = []
    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.in_script:
            self.scripts.append("".join(self.current))
            self.in_script = False
    def handle_data(self, data):
        if self.in_script:
            self.current.append(data)

source = Path("zarrin-arman/index.html").read_text(encoding="utf-8")
parser = Scripts()
parser.feed(source)
if not parser.scripts:
    print("No inline JavaScript found.")
    sys.exit(1)
for idx, script in enumerate(parser.scripts, start=1):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", encoding="utf-8") as f:
        f.write(script)
        f.flush()
        result = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
        if result.returncode:
            print(f"Script {idx} syntax check failed:\n{result.stderr}")
            sys.exit(result.returncode)
print(f"Inline JavaScript syntax passed: {len(parser.scripts)} script(s).")
