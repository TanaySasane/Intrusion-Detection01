import urllib.request, urllib.error, os

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
PROJECT = '/home/Tanay1202/Intrusion-Detection01'

def upload(remote, local):
    with open(local, 'rb') as f:
        content = f.read()
    boundary = 'PAbound99'
    fname = os.path.basename(local)
    body = ('--'+boundary+'\r\nContent-Disposition: form-data; name="content"; filename="'+fname+'"\r\nContent-Type: application/octet-stream\r\n\r\n').encode() + content + ('\r\n--'+boundary+'--\r\n').encode()
    headers = {'Authorization': 'Token '+TOKEN, 'Content-Type': 'multipart/form-data; boundary='+boundary}
    req = urllib.request.Request('https://www.pythonanywhere.com/api/v0/user/'+USERNAME+'/files/path'+remote, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp: return resp.status
    except urllib.error.HTTPError as e:
        if e.code in [200,201]: return e.code
        return e.code

print('Uploading images...')
for img in os.listdir('static/images'):
    local = os.path.join('static', 'images', img)
    # skip files with spaces or PDFs
    if ' ' in img or img.endswith('.pdf'):
        continue
    code = upload(f'{PROJECT}/static/images/{img}', local)
    print(f'  {img}: {code}')

print('\nUploading test_images...')
for img in os.listdir('static/test_images'):
    local = os.path.join('static', 'test_images', img)
    if ' ' in img: continue
    code = upload(f'{PROJECT}/static/test_images/{img}', local)
    print(f'  {img}: {code}')

print('\nDone!')
