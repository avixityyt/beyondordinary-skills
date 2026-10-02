"""Trusted data validation. This module never evaluates skill instructions."""
import datetime
import json
import re
import struct
import urllib.parse

SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
LOGIN = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?')

def jpeg_dimensions(data):
    if not data.startswith(b'\xff\xd8\xff'):
        raise ValueError('preview must be a JPEG')
    offset = 2
    while offset + 4 <= len(data):
        if data[offset] != 255:
            raise ValueError('invalid JPEG structure')
        while offset < len(data) and data[offset] == 255:
            offset += 1
        if offset >= len(data):
            break
        marker = data[offset]; offset += 1
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            continue
        if marker == 0xDA:
            break
        if offset + 2 > len(data):
            raise ValueError('truncated JPEG segment')
        size = struct.unpack('>H', data[offset:offset + 2])[0]
        if size < 2 or offset + size > len(data):
            raise ValueError('invalid JPEG segment')
        if marker in (0xC0, 0xC1, 0xC2):
            if size < 8:
                raise ValueError('invalid JPEG dimensions')
            height, width = struct.unpack('>HH', data[offset + 3:offset + 7])
            if not width or not height or width * height > 20_000_000:
                raise ValueError('preview exceeds 20 million pixels')
            return width, height
        offset += size
    raise ValueError('JPEG has no supported dimensions')

def validate_entry(slug, metadata, instructions, preview):
    if not isinstance(slug, str) or len(slug) > 80 or not SLUG.fullmatch(slug):
        raise ValueError('invalid slug')
    if not 1 <= len(metadata) <= 50_000 or not 1 <= len(instructions) <= 100_000 or not 1 <= len(preview) <= 2_000_000:
        raise ValueError('entry exceeds file size limits')
    item = json.loads(metadata.decode('utf-8-sig'))
    if not isinstance(item, dict) or item.get('slug') != slug:
        raise ValueError('slug must match its folder')
    limits = {'title':100,'summary':280,'author':100,'license':80,'distinctive':600,'limitations':600,'proof_note':600,'published':10}
    for key, limit in limits.items():
        if not isinstance(item.get(key), str) or not item[key].strip() or len(item[key]) > limit:
            raise ValueError('missing or oversized text: ' + key)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['published']):
        raise ValueError('published date must use YYYY-MM-DD')
    datetime.date.fromisoformat(item['published'])
    if item.get('category') not in ['Web design','Motion','Video','Creative coding']:
        raise ValueError('invalid category')
    for key, minimum, maximum, length in [('tools',1,8,60),('requirements',1,12,200),('steps',2,12,500)]:
        values = item.get(key)
        if not isinstance(values,list) or not minimum <= len(values) <= maximum or not all(isinstance(x,str) and x.strip() and len(x) <= length for x in values):
            raise ValueError('invalid ' + key)
    creator = item.get('creator')
    if not isinstance(creator,dict) or set(creator) != {'github_id','github_login','name'}:
        raise ValueError('include the creator identity')
    if not isinstance(creator['github_id'],str) or not re.fullmatch(r'[1-9][0-9]{0,19}',creator['github_id']):
        raise ValueError('creator ID must be a numeric string')
    if not isinstance(creator['github_login'],str) or not LOGIN.fullmatch(creator['github_login']):
        raise ValueError('invalid GitHub username')
    if not isinstance(creator['name'],str) or not 1 <= len(creator['name'].strip()) <= 100:
        raise ValueError('invalid creator name')
    for key in ['reviewed','rights_confirmed']:
        if not isinstance(item.get(key),bool):
            raise ValueError('review fields must be booleans')
    if not isinstance(item.get('demo'),str) or len(item['demo']) > 2000:
        raise ValueError('include an HTTPS result link')
    url = urllib.parse.urlsplit(item['demo'])
    if url.scheme != 'https' or not url.hostname or url.username or url.password:
        raise ValueError('result link must be HTTPS without credentials')
    if item.get('preview') != '/media/skills/' + slug + '.jpg':
        raise ValueError('preview path must match the slug')
    text = instructions.decode('utf-8-sig')
    frontmatter = re.match(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)',text,re.S)
    if not frontmatter or not re.search(r'^name:\s*' + re.escape(slug) + r'\s*$',frontmatter[1],re.M) or not re.search(r'^description:\s*\S.+$',frontmatter[1],re.M):
        raise ValueError('SKILL.md needs matching name and description frontmatter')
    jpeg_dimensions(preview)
    return item

def validate_tree(root, base=None, author_id=None, publisher_ids=()):
    """Validate bounded regular files, optionally compare creator changes with a PR base."""
    root = root.resolve()
    if (root/'skills').is_symlink() or not (root/'skills').is_dir() or (root/'previews').is_symlink():
        raise ValueError('skills and previews must be regular directories')
    entries = []
    folders = list((root/'skills').iterdir())
    if len(folders) > 500:
        raise ValueError('catalog exceeds 500 folders')
    for folder in folders:
        if folder.name.startswith('.'):
            continue
        if folder.is_symlink() or not folder.is_dir():
            raise ValueError('entry must be a regular directory: ' + folder.name)
        paths = [folder/'metadata.json',folder/'SKILL.md',root/'previews'/(folder.name+'.jpg')]
        blobs = []
        for path, limit in zip(paths,[50_000,100_000,2_000_000]):
            if path.is_symlink() or not path.is_file() or path.stat().st_size > limit or not path.resolve().is_relative_to(root):
                raise ValueError('missing, linked or oversized file: ' + str(path.relative_to(root)))
            blobs.append(path.read_bytes())
        item = validate_entry(folder.name,*blobs)
        if author_id and str(author_id) not in publisher_ids:
            previous = base/'skills'/folder.name/'metadata.json' if base else None
            old = json.loads(previous.read_text(encoding='utf-8-sig')) if previous and previous.is_file() and not previous.is_symlink() else {}
            if item['creator']['github_id'] != str(author_id) and item['creator'].get('github_id') != old.get('creator',{}).get('github_id'):
                raise ValueError('new creator credit must match the pull request author: ' + folder.name)
            if (item['reviewed'] or item['rights_confirmed']) and item != old:
                raise ValueError('contributors must leave review flags off: ' + folder.name)
        entries.append(item)
    return entries
