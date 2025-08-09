import json, urllib.request
REPO='T-O-C-A/PRO-tuner'
RAW=f'https://raw.githubusercontent.com/{REPO}/main/version.json'
CHLOG=f'https://raw.githubusercontent.com/{REPO}/main/CHANGELOG.md'
REL=f'https://github.com/{REPO}/releases/latest'
def check_updates(cur:str):
    try:
        with urllib.request.urlopen(RAW,timeout=4) as r: data=json.loads(r.read().decode())
        v=data.get('version','')
        if v and v!=cur:
            with urllib.request.urlopen(CHLOG,timeout=4) as r: log=r.read().decode()
            return {'latest':v,'changelog':log,'url':REL}
    except Exception: return None
    return None
