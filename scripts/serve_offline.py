"""Serve the checked-in website locally without external services."""
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8000);a=p.parse_args()
root=Path(__file__).resolve().parents[1]/'dist'
print(f'MQM local website: http://127.0.0.1:{a.port}/')
ThreadingHTTPServer(('127.0.0.1',a.port),partial(SimpleHTTPRequestHandler,directory=str(root))).serve_forever()
