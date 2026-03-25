import urllib.request, urllib.error, json

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'

paths = [
    f'/home/{USERNAME}/.virtualenvs/intrusion-venv/lib/',
    f'/home/{USERNAME}/.virtualenvs/intrusion-venv/lib/python3.11/site-packages/',
]

for path in paths:
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{path}'
    req = urllib.request.Request(url, headers={'Authorization': 'Token ' + TOKEN})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f'\n=== {path} ===')
            for name in list(data.keys())[:20]:
                print(f'  {name}')
    except urllib.error.HTTPError as e:
        print(f'{path}: {e.code}')
