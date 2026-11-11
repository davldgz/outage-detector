# outage-detector

## Goal and non-goals

Goal: This script checks a list of websites every 60 seconds and alerts me when one goes down or comes back up.

Non-goals (not in v1):
- No web UI
- No database
- No always-on deployment (will run in terminal)

## Decisions
- A site counts as down when: the request gets no response at all (timeout, DNS failure, connection refused) or server returns a 5xx status code
  - 4xx statuses (like 404) are logged but do not count as down
- Timeout: 5 seconds
- One check returns: a dict with four keys:
  - url: the site that was checked
  - status: the HTTP status code, or None if no response arrived
  - ms: response time in milliseconds, or None if no response arrived
  - error: a short description of what went wrong, or None if the request worked
  - Examples:
      - Success: {"url": "https://example.com", "status": 200, "ms": 143, "error": None}
      - Missing page: {"url": "https://example.com/nope", "status": 404, "ms": 98, "error": None}
      - Server error: {"url": "https://example.com", "status": 503, "ms": 210, "error": None}
      - Timeout: {"url": "https://example.com", "status": None, "ms": None, "error": "timeout"}
      - Bad domain: {"url": "https://exampel.com", "status": None, "ms": None, "error": "connection error"}
- Config: URLs and interval in config.json, ntfy topic in an environment variable

## Milestones
1. One check: a function that takes a URL and returns the result dict. Done when: calling it on a good URL, a 404 URL, and a nonexistent domain returns the correct dict for each, and none of them crashes the script.
2. Many URLs: read URLs from config.json and check each one. Done when: a list containing a good URL, a 404, a nonexistent domain, a slow URL (https://httpbin.org/delay/10), and a refused connection (http://localhost:9999) finishes without crashing and returns one correctly labeled dict per URL.
3. Logging: append timestamped results to a file. Done when: two separate runs leave one file containing both runs' lines, each line with a timestamp, url, status, ms, and error.
4. Loop and state: run repeatedly, track up/down per URL, alert only on changes. Done when: with a local test server running, stopping the server prints exactly one DOWN message, restarting it prints exactly one UP message, and nothing prints in between.
5. Alerts: send a real notification on changes. Done when: the DOWN and UP messages from milestone 4 arrive as push notifications on my phone, and the ntfy topic is not in any committed file.
