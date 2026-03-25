import urllib.request, urllib.error

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'

for logfile in [
    f'/var/log/tanay1202.pythonanywhere.com.error.log',
    f'/var/log/Tanay1202.pythonanywhere.com.error.log',
]:
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{logfile}'
    req = urllib.request.Request(url, headers={'Authorization': 'Token ' + TOKEN})
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode()
            print(f'=== {logfile} (last 3000 chars) ===')
            print(content[-3000:])
            break
    except urllib.error.HTTPError as e:
        print(f'{logfile}: {e.code}')
