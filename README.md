# Demo

A demo project for testing Claude Code.

## Setup

1. Install [Claude Code](https://github.com/anthropics/claude-code):
   ```bash
   npm install -g @anthropic/claude-code
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/Nagato988/demo.git
   cd demo
   ```

3. Authenticate with your Anthropic API key:
   ```bash
   claude
   ```

## Usage

Start an interactive Claude Code session in this directory:

```bash
claude
```

Use Claude Code to explore, modify, and experiment with code. Some things to try:

- Ask Claude to create or edit files
- Request code explanations or refactors
- Run commands and debug issues

## API Server

A simple HTTP API server is included (`api.py`).

### Start the server

```bash
python3 api.py
```

### Endpoints

#### `GET /healthz`

Returns the health status and version from `config.json`.

```bash
curl http://127.0.0.1:8080/healthz
# {"status": "ok", "version": "1.0.0"}
```

### Rate Limiting

All endpoints are rate-limited to **60 requests per minute per IP**.

When the limit is exceeded, the server returns:

```
HTTP 429 Too Many Requests
Retry-After: <seconds>
```

```bash
# Example: hitting the rate limit
for i in $(seq 1 61); do curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/healthz; done
# First 60: 200
# 61st: 429
```

### Run tests

```bash
python3 test_api.py
```
