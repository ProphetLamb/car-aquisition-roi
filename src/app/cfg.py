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
    global api_endpoint

    load_dotenv()
    client_id = os.getenv('CAR_CLIENT_ID')
    assert client_id, "A shared client id between the server and client is required"

    debug = os.getenv('DEBUG', False)
    debug = True if debug else False

    origin = os.getenv('ORIGIN', 'http://127.0.0.1:3001').split(',')
    assert len(origin) > 0, "At least one origin must be specified in the ORIGIN environment variable"

    host = os.getenv('APP_ENDPOINT', 'http://127.0.0.1:3001')
    host = host.split('//')[1]
    host, port = host.split(':')
    port = int(port) if port else None
    assert host, "A host must be specified in the APP_ENDPOINT environment variable"
    assert port, "A port must be specified in the APP_ENDPOINT environment variable"

    api_endpoint = os.getenv('API_ENDPOINT', 'http://127.0.0.1:3000')
    assert api_endpoint, "A api endpoint must be specified in the API_ENDPOINT environment variable"
