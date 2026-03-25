import urllib.request, urllib.error, json

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'

# Read setup.log
url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path/home/{USERNAME}/setup.log'
headers = {'Authorization': 'Token ' + TOKEN}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        print('=== setup.log ===')
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('Log not found:', e.code)

# Check if venv exists
url2 = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path/home/{USERNAME}/.virtualenvs/'
req2 = urllib.request.Request(url2, headers=headers)
try:
    with urllib.request.urlopen(req2) as resp:
        print('\n=== .virtualenvs/ ===')
        print(resp.read().decode()[:500])
except urllib.error.HTTPError as e:
    print('venvs dir:', e.code)
