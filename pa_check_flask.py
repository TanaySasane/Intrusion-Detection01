import urllib.request, urllib.error, json

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'

url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path/home/{USERNAME}/.virtualenvs/intrusion-venv/lib/python3.11/site-packages/'
req = urllib.request.Request(url, headers={'Authorization': 'Token ' + TOKEN})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    packages = sorted(data.keys())
    print('All packages:')
    for p in packages:
        print(' ', p)
