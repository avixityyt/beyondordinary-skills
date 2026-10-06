"""Read-only submission boundaries and review signals. Never run submitted code."""
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

REPOSITORY = 'avixityyt/beyondordinary-skills'
PUBLISHER_IDS = {'74422918'}
SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')

def allowed_path(value):
    parts = value.split('/')
    if any(not part or part.startswith('.') for part in parts):
        return False
    return ((len(parts) >= 3 and parts[0] == 'skills' and len(parts[1]) <= 80 and SLUG.fullmatch(parts[1]) is not None)
        or (len(parts) == 2 and parts[0] == 'previews' and parts[1].endswith('.jpg') and SLUG.fullmatch(parts[1][:-4]) is not None))

def check_files(root, files, author_id):
    if len(files) > 60:
        raise ValueError('Split this submission into smaller changes: at most 60 changed files per PR.')
    total = 0
    for item in files:
        for name in [item['filename'], item.get('previous_filename')]:
            if name is None:
                continue
            if str(author_id) not in PUBLISHER_IDS and not allowed_path(name):
                raise ValueError('Contributor PRs may change only skill folders and JPEG previews. Workflow, tooling and documentation changes need a separate owner-reviewed PR.')
            path = root / name
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError('Linked files and paths outside the submission are not allowed.')
            if path.is_file():
                if path.stat().st_size > 2_000_000:
                    raise ValueError('Keep each changed file under 2,000,000 bytes; link larger results instead.')
                total += path.stat().st_size
    if total > 5_000_000:
        raise ValueError('Keep changed submission files under 5,000,000 bytes in total; link larger results instead.')

def signals(user, pulls, author_id, now):
    flags = []
    if user.get('type') == 'Bot':
        flags.append('Automated account: confirm the human creator and submission permissions.')
    created = user.get('created_at')
    if created:
        age = now - datetime.datetime.fromisoformat(created.replace('Z', '+00:00'))
        if age < datetime.timedelta(days=7):
            flags.append('GitHub account is under seven days old: review identity and proof carefully.')
    recent = [pull for pull in pulls if str(pull.get('user', {}).get('id')) == str(author_id)
        and now - datetime.datetime.fromisoformat(pull['created_at'].replace('Z', '+00:00')) < datetime.timedelta(days=1)]
    if len(recent) >= 4:
        flags.append('Four or more PRs from this identity in the last day: check for repetitive submissions.')
    return flags

def duplicates(root, base, files):
    fingerprints = {}
    for path in sorted((base / 'skills').glob('*/SKILL.md')):
        if not path.is_symlink() and path.is_file() and path.stat().st_size <= 100_000:
            body = re.sub(r'^---\r?\n.*?\r?\n---\r?\n?', '', path.read_text(encoding='utf-8-sig'), count=1, flags=re.S)
            normalized = ' '.join(body.split())
            if normalized:
                fingerprints.setdefault(hashlib.sha256(normalized.encode()).hexdigest(), set()).add(path.parent.name)
    flagged = False
    for item in files:
        name = item['filename'];path = root / name
        if not allowed_path(name) or path.name != 'SKILL.md' or item.get('status') == 'removed':
            continue
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 100_000:
            continue
        body = re.sub(r'^---\r?\n.*?\r?\n---\r?\n?', '', path.read_text(encoding='utf-8-sig'), count=1, flags=re.S)
        normalized = ' '.join(body.split())
        if not normalized:
            continue
        fingerprint = hashlib.sha256(normalized.encode()).hexdigest()
        if fingerprints.get(fingerprint, set()) - {path.parent.name}:
            flagged = True
        fingerprints.setdefault(fingerprint, set()).add(path.parent.name)
    return ['Duplicate instruction body detected under a different slug: inspect whether this is a distinct contribution.'] if flagged else []

def api(path):
    headers = {'Accept':'application/vnd.github+json','User-Agent':'Beyond-Ordinary-submission-review','X-GitHub-Api-Version':'2026-03-10'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    request = urllib.request.Request('https://api.github.com/' + path, headers=headers)
    with urllib.request.urlopen(request, timeout=15) as response:
        raw = response.read(2_000_001)
    if len(raw) > 2_000_000:
        raise ValueError('GitHub response exceeds the review limit.')
    return json.loads(raw)

def main():
    root, base = [pathlib.Path(value).resolve() for value in sys.argv[1:3]]
    event = json.loads(pathlib.Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    pull = event.get('pull_request')
    if not pull:
        print('Review signals run on pull requests only.');return
    if pull['base']['repo']['full_name'] != REPOSITORY:
        raise ValueError('Unexpected base repository.')
    number = int(pull['number']);author_id = str(pull['user']['id'])
    files = []
    for page in [1, 2, 3]:
        batch = api(f'repos/{REPOSITORY}/pulls/{number}/files?per_page=30&page={page}')
        files.extend(batch)
        if len(files) > 60 or len(batch) < 30:
            break
    check_files(root, files, author_id)
    login = urllib.parse.quote(pull['user']['login'], safe='')
    user = api('users/' + login)
    if str(user.get('id')) != author_id:
        raise ValueError('Creator identity lookup did not match the PR author.')
    pulls = api(f'repos/{REPOSITORY}/pulls?state=all&sort=created&direction=desc&per_page=100')
    now = datetime.datetime.now(datetime.timezone.utc)
    flags = signals(user, pulls, author_id, now) + duplicates(root, base, files)
    if len(pulls) == 100:
        flags.append('Recent activity scan reached 100 PRs; review burst activity manually if needed.')
    summary = '## Submission review\n\nFile boundaries and size checks passed.\n\n'
    summary += '\n'.join('- ' + flag for flag in flags) if flags else 'No account-age, burst or duplicate-body signals were found in this bounded check.'
    summary += '\n\nThese signals request human review. They do not automatically reject, ban, label or message anyone. Passing checks do not prove rights, originality or safety.\n'
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as stream:stream.write(summary)
    print(summary)

if __name__ == '__main__':
    try:main()
    except Exception:
        # API requests may carry credentials; keep exception bodies out of logs.
        print('::error::Submission review could not complete. Check allowed files, file sizes and API availability. Maintainer review is required.')
        sys.exit(1)
