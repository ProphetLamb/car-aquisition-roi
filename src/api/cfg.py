import os
from dotenv import load_dotenv

client_id: str
debug: bool
origin: list
host: str
port: int

def load():
    global client_id
    global debug
    global origin
    global host
    global port

    load_dotenv()
    client_id = os.getenv('CAR_CLIENT_ID')
    assert client_id, "A shared client id between the server and client is required"

    debug = os.getenv('DEBUG', False)
    debug = True if debug else False

    origin = os.getenv('ORIGIN', 'http://127.0.0.1:3001').split(',')
    assert len(origin) > 0, "At least one origin must be specified in the ORIGIN environment variable"

    host = os.getenv('API_ENDPOINT', 'http://127.0.0.1:3000')
    host = host.split('//')[1]
    host, port = host.split(':')
    port = int(port) if port else None
    assert host, "A host must be specified in the first origin"
    assert port, "A port must be specified in the first origin"
