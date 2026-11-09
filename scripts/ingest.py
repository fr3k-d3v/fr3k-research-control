#!/usr/bin/env python3
"""Bounded, read-only local research inventory. No network, GPU or secret ingestion."""
import argparse, hashlib, json, os, pathlib, re, sys, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
DEFAULT=[pathlib.Path.home()/ 'Documents'/name for name in ('FR3K-HARDWARE-MAXIMIZATION-SCOUT','FR3K-RESEARCH-STAGING-2026-11-09','FR3K-EXTERNAL-RESEARCH-2026-11-09')]
BLOCK=re.compile(r'(token|secret|password|credential|\.env|private|key|\.pem|\.sqlite|\.db)',re.I)
def collect(roots,max_files=500,max_bytes=2_000_000):
 out=[]
 for root in roots:
  if not root.is_dir():continue
  for path in sorted(root.rglob('*')):
   if len(out)>=max_files:return out
   if path.is_symlink() or not path.is_file() or path.suffix.lower() not in ('.md','.json','.txt') or BLOCK.search(path.name):continue
   try:
    stat=path.stat()
    if stat.st_size>max_bytes:continue
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    out.append({'collection':root.name,'relative_path':str(path.relative_to(root)),'sha256':digest,'bytes':stat.st_size,'modified_utc':int(stat.st_mtime)})
   except (OSError,ValueError):continue
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'ledger'/'research-manifest.json'));p.add_argument('--root',action='append');a=p.parse_args()
 roots=[pathlib.Path(x).expanduser().resolve() for x in a.root] if a.root else DEFAULT
 entries=collect(roots)
 data={'schema':1,'generated_utc':int(time.time()),'mode':'metadata-only','source':'Omarchy research folders','count':len(entries),'entries':entries}
 target=pathlib.Path(a.output);target.parent.mkdir(parents=True,exist_ok=True)
 temp=target.with_suffix('.tmp');temp.write_text(json.dumps(data,indent=2)+'\n');os.replace(temp,target)
 print(json.dumps({'count':len(entries),'output':str(target)}))
if __name__=='__main__':main()
