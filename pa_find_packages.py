import urllib.request, urllib.error, json

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'

# PA has managed Python environments - check common paths
paths_to_check = [
    '/usr/lib/python3.11/',
    '/usr/lib/python3.11/dist-packages/',
    '/usr/local/lib/python3.11/',
    '/usr/local/lib/python3.11/dist-packages/',
    '/home/Tanay1202/.local/lib/python3.11/',
    '/home/Tanay1202/.local/lib/python3.11/site-packages/',
]

for path in paths_to_check:
    url = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME + '/files/path' + path
    req = urllib.request.Request(url, headers={'Authorization': 'Token ' + TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            pkgs = [k for k in data.keys() if any(x in k.lower() for x in ['numpy','pandas','sklearn','scipy','flask'])]
            print(f'{path}')
            print(f'  relevant: {pkgs}')
            print(f'  total items: {len(data)}')
    except Exception as e:
        print(f'{path}: {str(e)[:60]}')
