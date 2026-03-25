import urllib.request, urllib.error, os

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
VENV_PANDAS = '/home/Tanay1202/.virtualenvs/intrusion-venv/lib/python3.11/site-packages/pandas'
LOCAL_PANDAS = r'C:\Users\Dell\AppData\Roaming\Python\Python314\site-packages\pandas'

def upload_bytes(remote_path, content, fname='file'):
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}'
    boundary = 'PAbound99'
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="{fname}"\r\nContent-Type: application/octet-stream\r\n\r\n').encode() + content + (f'\r\n--{boundary}--\r\n').encode()
    headers = {'Authorization': 'Token ' + TOKEN, 'Content-Type': f'multipart/form-data; boundary={boundary}'}
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code

# Upload missing pandas directories: _config, api, arrays, tseries
missing_dirs = ['_config', 'api', 'arrays', 'tseries']

for d in missing_dirs:
    local_dir = os.path.join(LOCAL_PANDAS, d)
    if not os.path.exists(local_dir):
        print(f'  {d}: not found locally')
        continue
    print(f'\nUploading pandas/{d}...')
    for root, dirs, files in os.walk(local_dir):
        for fname in files:
            if fname.endswith('.so') or fname.endswith('.pyd'):
                continue  # skip compiled extensions - wrong platform
            local_path = os.path.join(root, fname)
            rel = os.path.relpath(local_path, LOCAL_PANDAS).replace('\\', '/')
            remote = f'{VENV_PANDAS}/{rel}'
            with open(local_path, 'rb') as f:
                content = f.read()
            code = upload_bytes(remote, content, fname)
            print(f'  {rel}: {code}')

# Also upload missing pandas/__init__ items
print('\nUploading pandas top-level missing files...')
for fname in ['__init__.py']:
    local_path = os.path.join(LOCAL_PANDAS, fname)
    if os.path.exists(local_path):
        with open(local_path, 'rb') as f:
            content = f.read()
        code = upload_bytes(f'{VENV_PANDAS}/{fname}', content, fname)
        print(f'  {fname}: {code}')

print('\nDone uploading pandas fixes!')
