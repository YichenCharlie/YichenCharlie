"""Build profile statistics from public GitHub repository metadata."""
import json
import os
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from html import escape

ROOT = Path(__file__).resolve().parents[1]
USER = 'YichenCharlie'

def fetch_repos():
    repos = []
    for page in range(1, 101):
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-stats'}
        if os.getenv('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
        request = Request(f'https://api.github.com/users/{USER}/repos?per_page=100&page={page}', headers=headers)
        with urlopen(request, timeout=30) as response:
            batch = json.load(response)
        repos.extend(batch)
        if len(batch) < 100:
            return repos
    raise RuntimeError('Repository pagination limit exceeded')

def fetch_language_totals(repos):
    totals = Counter()
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-stats'}
    if os.getenv('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    for repo in repos:
        if repo['fork'] or repo['name'].lower() == USER.lower():
            continue
        request = Request(f"https://api.github.com/repos/{USER}/{repo['name']}/languages", headers=headers)
        with urlopen(request, timeout=30) as response:
            totals.update(json.load(response))
    return totals

def build(totals, now):
    total = sum(totals.values())
    rows = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    lines = ['Languages across my public code', '']
    for language, size in rows[:5]:
        ratio = size / total if total else 0
        filled = round(ratio * 25)
        bar = '█' * filled + '─' * (25 - filled)
        lines.append(f'{language:<20} {bar}   {ratio * 100:6.2f} %')
    if not rows:
        lines.append('No language data available yet.')
    return '```text\n' + '\n'.join(lines) + '\n```\n\n' + (
        '<sub>Top 5 languages; percentages use all language bytes. Excludes forks and this profile. '
        'Notebook files are counted separately; includes starter code. '
        f'Updated {now:%Y-%m-%d} UTC.</sub>'
    )

START = '<!-- STATS:START -->'
END = '<!-- STATS:END -->'

def update_readme(readme, result):
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError('Expected one stats marker pair in README')
    before, rest = readme.split(START)
    _, after = rest.split(END)
    return before + START + "\n" + result + "\n" + END + after

if __name__ == '__main__':
    result = build(fetch_language_totals(fetch_repos()), datetime.now(timezone.utc))
    target = ROOT / 'README.md'
    target.write_text(update_readme(target.read_text(encoding='utf-8'), result), encoding='utf-8')
    print('Updated README text statistics.')
