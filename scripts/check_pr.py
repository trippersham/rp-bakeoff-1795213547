"""Minimal faithful stand-in for the real scripts/check_pr.py.

Validates that a PR body carries the six ordered H2 sections, an issue
reference, and the attribution footer. Reads --event <github event json>.
This is the gate release-please's auto-generated PR body must clear.
"""

import json
import re
import sys

REQUIRED_SECTIONS = [
    '## Tasks',
    '## What changed',
    '## Proof',
    '## Limits',
    '## Release impact',
    '## Agent context',
]


def main() -> None:
    idx = sys.argv.index('--event')
    with open(sys.argv[idx + 1]) as f:
        event = json.load(f)
    pull_request = event.get('pull_request')
    if not isinstance(pull_request, dict) or 'body' not in pull_request:
        raise ValueError('event JSON has no pull_request.body')
    body = pull_request['body'] or ''
    missing = [h for h in REQUIRED_SECTIONS if h not in body]
    if missing:
        raise SystemExit(f'PR body is missing sections: {missing}')
    if not re.search(r'(Closes|Part of) #\d+', body):
        raise SystemExit('PR body has no issue reference (Closes #N / Part of #N)')
    if 'Posted on behalf of' not in body:
        raise SystemExit('PR body has no attribution footer')
    print('pr-body ok')


if __name__ == '__main__':
    main()
