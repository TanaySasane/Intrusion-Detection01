import urllib.request, urllib.error, json, time, urllib.parse

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
PROJECT = '/home/Tanay1202/Intrusion-Detection01'
DOMAIN = 'Tanay1202.pythonanywhere.com'

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

# Upload the existing db.db (creates the directory automatically)
print('[1] Uploading database/db.db...')
with open('database/db.db', 'rb') as f:
    content = f.read()
code = upload_bytes(f'{PROJECT}/database/db.db', content, 'db.db')
print(f'  db.db: {code}')

# Reload
print('[2] Reloading...')
req = urllib.request.Request(
    f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/webapps/{DOMAIN}/reload/',
    headers={'Authorization': 'Token ' + TOKEN}, method='POST'
)
with urllib.request.urlopen(req) as resp:
    print(' ', resp.read().decode())

time.sleep(6)

# Test
print('[3] Testing...')
req2 = urllib.request.Request('https://Tanay1202.pythonanywhere.com', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req2, timeout=15) as resp:
        body = resp.read().decode()
        if 'Hello, World' in body:
            print('Still default page')
        elif 'Internal Server Error' in body or '500' in body:
            print('500 error still')
        else:
            print('SUCCESS! App is live!')
            print(body[:400])
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    body = e.read().decode()
    if '500' in str(e.code):
        print('Still 500 - check error log')
