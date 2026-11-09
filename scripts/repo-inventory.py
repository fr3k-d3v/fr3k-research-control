#!/usr/bin/env python3
"""Public GitHub inventory via gh CLI. Does not clone or expose credentials."""
import datetime,json,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[1]
p=subprocess.run(['gh','repo','list','fr3k-d3v','--limit','100','--json','name,url,pushedAt,isPrivate'],capture_output=True,text=True,check=True)
repos=json.loads(p.stdout)
rows=[{'name':x['name'],'url':x['url'],'pushed_at':x['pushedAt'],'visibility':'private' if x['isPrivate'] else 'public','mirror_status':'NOT_VERIFIED'} for x in repos]
out=root/'ledger'/'github-repos.json';out.write_text(json.dumps({'schema':1,'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(rows),'repositories':rows},indent=2)+'\n');print('Inventoried',len(rows),'repos; mirror status unverified')
