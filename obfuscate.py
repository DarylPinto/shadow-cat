import os
import json
import subprocess
from base64 import encodebytes, decodebytes
from itertools import cycle

def sys_encode(dict):
	string = json.dumps(dict)
	string = encodebytes(string.encode()).decode()
	key = os.popen('wmic csproduct get uuid').read().strip().split('\n')[2].strip()
	return ''.join(chr(ord(c)^ord(k)) for c,k in zip(string, cycle(key)))

def sys_decode(encoded):
	key = os.popen('wmic csproduct get uuid').read().strip().split('\n')[2].strip()
	string = ''.join(chr(ord(c)^ord(k)) for c,k in zip(encoded, cycle(key)))
	string = decodebytes(string.encode())
	return json.loads(string)

def decode(encoded):
	string = decodebytes(encoded.encode())
	return json.loads(string)
