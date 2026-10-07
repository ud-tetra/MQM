"""Execute the canonical notebook without Jupyter, then compare expected JSON."""
import contextlib,io,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
nb=json.loads((root/'artifacts/subsystem_algebra.ipynb').read_text())
ns={};out=io.StringIO()
with contextlib.redirect_stdout(out):
    for cell in nb['cells']:
        if cell['cell_type']=='code':exec(compile(''.join(cell['source']),'subsystem_algebra.ipynb','exec'),ns)
actual=json.loads(out.getvalue())
expected=root/'expected/subsystem_algebra.json'
if expected.exists():assert actual==json.loads(expected.read_text())
print(out.getvalue(),end='')
