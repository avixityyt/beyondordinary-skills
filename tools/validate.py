import json,pathlib,re,sys,urllib.parse
root=pathlib.Path(sys.argv[1]).resolve()
errors=[]
for file in (root/'skills').glob('*/metadata.json'):
    try:
        if file.is_symlink() or file.stat().st_size>50000: raise ValueError('metadata must be a bounded regular file')
        item=json.loads(file.read_text(encoding='utf-8-sig'))
        slug=item['slug']
        creator=item.get('creator')
        if not isinstance(creator,dict) or set(creator)!={'github_id','github_login','name'}: raise ValueError('include creator identity')
        if not isinstance(creator['github_id'],str) or not re.fullmatch(r'[1-9][0-9]{0,19}',creator['github_id']): raise ValueError('creator github_id must be a numeric ID string')
        if not isinstance(creator['github_login'],str) or not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?',creator['github_login']): raise ValueError('invalid creator github_login')
        if not isinstance(creator['name'],str) or not 1<=len(creator['name'].strip())<=100: raise ValueError('invalid creator name')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug) or slug!=file.parent.name: raise ValueError('invalid slug')
        for key in ['title','summary','author','license','distinctive','limitations','proof_note','published']:
            if not isinstance(item.get(key),str) or not item[key].strip() or len(item[key])>1000: raise ValueError('missing or oversized text: '+key)
        if item['category'] not in ['Web design','Motion','Video','Creative coding']: raise ValueError('invalid category')
        for key in ['tools','requirements','steps']:
            if not isinstance(item.get(key),list) or not item[key] or len(item[key])>12 or not all(isinstance(x,str) and 0<len(x)<=600 for x in item[key]): raise ValueError('invalid '+key)
        for key in ['reviewed','rights_confirmed']:
            if not isinstance(item.get(key),bool): raise ValueError('review fields must be booleans')
        url=urllib.parse.urlparse(item['demo'])
        if not (url.scheme=='https' and url.hostname and not url.username and not url.password): raise ValueError('demo must be an HTTPS link')
        if item['preview']!='/media/skills/'+slug+'.jpg': raise ValueError('preview path must match slug')
        preview=root/'previews'/(slug+'.jpg')
        if not preview.is_file() or preview.is_symlink() or preview.stat().st_size>2000000: raise ValueError('missing or oversized JPEG preview')
        skill=file.parent/'SKILL.md'
        if not skill.is_file() or skill.is_symlink() or not 1<=skill.stat().st_size<=100000: raise ValueError('missing or oversized SKILL.md')
        if not skill.read_text(encoding='utf-8-sig').startswith('---'): raise ValueError('include skill frontmatter')
    except (ValueError,KeyError,OSError,TypeError) as e: errors.append(str(file.relative_to(root))+': '+str(e))
if errors:
    print('\n'.join(errors));sys.exit(1)
print('Structure validated. No skill was executed. Human review is still required.')
