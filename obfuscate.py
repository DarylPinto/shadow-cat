import os
import platform
import json
import subprocess
from base64 import encodebytes, decodebytes
from itertools import cycle

def hwid():
	if platform.system() == "Windows":
		return os.popen('wmic csproduct get uuid').read().strip().split('\n')[2].strip()
	elif platform.system() == "Darwin":
		return os.popen("/usr/sbin/system_profiler SPHardwareDataType | fgrep 'Serial' | awk '{print $NF}'")
	else:
		return "123XYZ"

def sys_encode(dict):
	string = json.dumps(dict)
	string = encodebytes(string.encode()).decode()
	key = hwid()
	return ''.join(chr(ord(c)^ord(k)) for c,k in zip(string, cycle(key)))

def sys_decode(encoded):
	key = hwid()
	string = ''.join(chr(ord(c)^ord(k)) for c,k in zip(encoded, cycle(key)))
	string = decodebytes(string.encode())
	return json.loads(string)

def decode(encoded):
	string = decodebytes(encoded.encode())
	return json.loads(string)
