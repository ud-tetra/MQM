"""Verify package hashes and both canonical replay results; no network or QPU calls."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MANIFEST_SHA256.json').read_text())
for path,digest in manifest.items():
    p=root/path
    assert p.resolve().is_relative_to(root.resolve()),path
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,path
for command,expected in [('support/run_notebook.py','subsystem_algebra.json'),('artifacts/x5_envelope.py','x5_envelope.json')]:
    run=subprocess.run([sys.executable,'-B',str(root/command)],cwd=root,check=True,capture_output=True,text=True)
    assert json.loads(run.stdout)==json.loads((root/'expected'/expected).read_text()),command
print(json.dumps({'manifest_entries':len(manifest),'canonical_replays':2,'status':'PASS'},indent=2))
