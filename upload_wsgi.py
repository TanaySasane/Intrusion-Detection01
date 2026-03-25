import urllib.request, urllib.error

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
PROJECT_DIR = '/home/Tanay1202/Intrusion-Detection01'

# Use PA's system site-packages which has numpy/pandas/sklearn/flask pre-installed
WSGI_CONTENT = (
    "import sys, os\n"
    "\n"
    "# Project path\n"
    "path = '" + PROJECT_DIR + "'\n"
    "if path not in sys.path:\n"
    "    sys.path.insert(0, path)\n"
    "\n"
    "# Use PA's pre-installed packages (numpy, pandas, sklearn, flask)\n"
    "pa_packages = '/usr/local/lib/python3.11/site-packages'\n"
    "if pa_packages not in sys.path:\n"
    "    sys.path.insert(1, pa_packages)\n"
    "\n"
    "os.environ['SECRET_KEY'] = 'intrusion-detection-pa-2026'\n"
    "\n"
    "from app import app as application\n"
)

boundary = 'PAboundary123456789'
body = (
    '--' + boundary + '\r\n'
    'Content-Disposition: form-data; name="content"; filename="wsgi.py"\r\n'
    'Content-Type: application/octet-stream\r\n\r\n'
).encode() + WSGI_CONTENT.encode() + ('\r\n--' + boundary + '--\r\n').encode()

headers = {
    'Authorization': 'Token ' + TOKEN,
    'Content-Type': 'multipart/form-data; boundary=' + boundary
}

for wsgi_path in [
    '/var/www/' + USERNAME + '_pythonanywhere_com_wsgi.py',
    '/var/www/tanay1202_pythonanywhere_com_wsgi.py',
]:
    url = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME + '/files/path' + wsgi_path
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            print('Uploaded ' + wsgi_path + ':', resp.status)
    except urllib.error.HTTPError as e:
        print('Uploaded ' + wsgi_path + ':', e.code)
