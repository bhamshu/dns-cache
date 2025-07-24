# dns-cache

DNS cache with TTL expiration + LRU eviction. Backed by a DLL (for LRU) and a SortedList (expiry-ordered index). This version:
- **Removes the `seq` tie-breaker** (uses only `(expires_at, domain)`)
- Adds an **IPv4 validator**
- Wraps the expiry tuple into a **`BSTKey` dataclass**
- Ships a `requirements.txt` that **includes pytest**
- Shows how to set up the project using **uv**

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
