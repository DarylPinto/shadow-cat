import json
from base64 import encodebytes, decodebytes

encode = lambda dict : encodebytes(json.dumps(dict).encode()).decode().strip()[::-1]
decode = lambda encoded : json.loads(decodebytes(encoded[::-1].encode()))
