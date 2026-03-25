import urllib.request, urllib.error, urllib.parse, json, time

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
DOMAIN = 'Tanay1202.pythonanywhere.com'
PROJECT = '/home/Tanay1202/Intrusion-Detection01'
BASE = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
HEADERS = {'Authorization': 'Token ' + TOKEN}

def api(path, method='GET', data=None, json_data=None):
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
            try: return True, json.loads(txt)
            except: return True, txt
    except urllib.error.HTTPError as e:
        return False, f'HTTP {e.code}: {e.read().decode()[:200]}'

def upload_text(remote_path, content):
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}'
    boundary = 'PAbound99'
    fname = remote_path.split('/')[-1]
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="{fname}"\r\nContent-Type: text/plain\r\n\r\n').encode() + content.encode() + (f'\r\n--{boundary}--\r\n').encode()
    headers = {'Authorization': 'Token ' + TOKEN, 'Content-Type': f'multipart/form-data; boundary={boundary}'}
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp: return resp.status
    except urllib.error.HTTPError as e: return e.code

# Upload a git-pull + reload script to PA
pull_script = f"""#!/bin/bash
cd {PROJECT}
git pull origin main
echo "Pulled from GitHub"
"""

print('[1] Uploading git-pull script...')
code = upload_text(f'/home/{USERNAME}/git_pull.sh', pull_script)
print(f'  git_pull.sh: {code}')

# Upload a Python webhook handler that PA can serve
webhook_app = f"""import subprocess, hmac, hashlib, os
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET = os.environ.get('GITHUB_SECRET', 'intrusion-webhook-secret')

@app.route('/webhook', methods=['POST'])
def webhook():
    sig = request.headers.get('X-Hub-Signature-256', '')
    body = request.get_data()
    expected = 'sha256=' + hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return jsonify({{'error': 'Invalid signature'}}), 403
    result = subprocess.run(['git', '-C', '{PROJECT}', 'pull', 'origin', 'main'],
                          capture_output=True, text=True)
    # Reload web app
    import urllib.request
    req = urllib.request.Request(
        'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/webapps/{DOMAIN}/reload/',
        headers={{'Authorization': 'Token {TOKEN}'}}, method='POST'
    )
    urllib.request.urlopen(req)
    return jsonify({{'status': 'ok', 'output': result.stdout}})

if __name__ == '__main__':
    app.run()
"""

# Instead - simpler approach: just do git pull via console now
print('\n[2] Clearing old consoles...')
ok, consoles = api('/consoles/')
if ok and isinstance(consoles, list):
    for c in consoles:
        api(f'/consoles/{c["id"]}/', method='DELETE')
        time.sleep(0.5)
    print(f'  Cleared {len(consoles)}')

print('\n[3] Creating bash console...')
ok, result = api('/consoles/', method='POST', data={'executable': 'bash', 'working_directory': f'/home/{USERNAME}'})
if not ok or not isinstance(result, dict):
    print('Failed:', result); exit(1)
cid = result['id']
print(f'  Console: {cid}')
time.sleep(5)

def send(cmd):
    api(f'/consoles/{cid}/send_input/', method='POST', json_data={'input': cmd + '\n'})

# Initialize git repo on PA and pull
print('\n[4] Setting up git on PA...')
send(f'cd {PROJECT} && git init && git remote add origin https://github.com/TanaySasane/Intrusion-Detection01.git 2>/dev/null || true && git remote set-url origin https://github.com/TanaySasane/Intrusion-Detection01.git && git fetch origin main && git reset --hard origin/main && echo GIT_DONE')
print('  Sent git setup command, waiting 30s...')
time.sleep(30)

# Reload web app
print('\n[5] Reloading web app...')
ok, r = api(f'/webapps/{DOMAIN}/reload/', method='POST')
print(f'  {"Reloaded!" if ok else r}')

api(f'/consoles/{cid}/', method='DELETE')
print('\nDone! PA is now synced with GitHub.')
print('To sync again anytime, just run: python pa_git_sync.py')
