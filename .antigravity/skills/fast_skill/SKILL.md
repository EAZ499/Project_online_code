---
name: fast_read
description: Fast whole-file reader that reads complete files in a single pass without pagination.
---

# Instructions
When reading the file specified by the user:
1. Do not use chunked pagination.
2. Execute a single shell command to display the content:
   - On Windows: `Get-Content -Path "<path>" -Raw`
   - On Linux/macOS: `cat "<path>"`
3. If terminal execution is unavailable, call the native file reading tool with `start_line: 1` and `limit: 5000`.
4. Proceed immediately to analyzing the file content.