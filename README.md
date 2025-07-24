# dns-cache

## Quick start (with `uv`)

```bash
# 1) Install uv (https://github.com/astral-sh/uv)
curl -Ls https://astral.sh/uv/install.sh | sh

# 2) Create & activate venv
cd dns-cache
uv venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

# 3) Install deps & run tests
uv pip install -e .
uv pip install -r requirements.txt
uv run pytest -q
```
