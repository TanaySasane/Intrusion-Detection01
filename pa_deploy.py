"""
PythonAnywhere full deployment script
"""
import urllib.request, urllib.error, urllib.parse
import json, os, time

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
BASE = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
HEADERS = {'Authorization': 'Token ' + TOKEN}

def api(path, method='GET', data=None, json_data=None, files=None):
    url = BASE + path
    headers = dict(HEADERS)
    body = None
    if json_data is not None:
        headers['Content-Type'] = 'application/json'
        body = json.dumps(json_data).encode()
    elif data is not None:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            txt = resp.read().decode()
            try: return json.loads(txt)
            except: return txt
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f'  HTTP {e.code}: {err[:200]}')
        return None

def upload_file(remote_path, local_path):
    """Upload a file using multipart form"""
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}'
    with open(local_path, 'rb') as f:
        content = f.read()
    boundary = '----FormBoundary7MA4YWxkTrZu0gW'
    filename = os.path.basename(local_path)
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="content"; filename="{filename}"\r\n'
        f'Content-Type: application/octet-stream\r\n\r\n'
    ).encode() + content + f'\r\n--{boundary}--\r\n'.encode()
    headers = dict(HEADERS)
    headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        # 200 or 201 = success
        if e.code in [200, 201]:
            return e.code
        print(f'  Upload error {e.code}: {e.read().decode()[:100]}')
        return e.code

def run_bash(cmd):
    """Run a bash command via scheduled task workaround using always-on or consoles"""
    # Create a new console
    result = api('/consoles/', method='POST', data={'executable': 'bash', 'working_directory': '/home/' + USERNAME})
    if not result:
        return None
    cid = result['id']
    time.sleep(3)
    # Send command
    api(f'/consoles/{cid}/send_input/', method='POST', json_data={'input': cmd + '\n'})
    time.sleep(8)
    # Get output
    out = api(f'/consoles/{cid}/get_latest_output/')
    # Kill console
    api(f'/consoles/{cid}/', method='DELETE')
    return out.get('output', '') if isinstance(out, dict) else str(out)

print('='*50)
print('PythonAnywhere Deployment')
print('='*50)

# Step 1: Upload key files
print('\n[1] Uploading files...')
files_to_upload = [
    ('app.py', '/home/Tanay1202/Intrusion-Detection01/app.py'),
    ('Database.py', '/home/Tanay1202/Intrusion-Detection01/Database.py'),
    ('init_db.py', '/home/Tanay1202/Intrusion-Detection01/init_db.py'),
    ('requirements.txt', '/home/Tanay1202/Intrusion-Detection01/requirements.txt'),
]
for local, remote in files_to_upload:
    if os.path.exists(local):
        code = upload_file(remote, local)
        print(f'  {local} -> {code}')

print('\nDone. Check console output above.')
print('Next: configure web app via dashboard at https://www.pythonanywhere.com')
