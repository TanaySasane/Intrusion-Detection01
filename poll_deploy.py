import urllib.request, json, time

svc_id = 'srv-d71436ffte5s739sskr0'
headers = {
    'Authorization': 'Bearer rnd_WW57IbqJ3KxRpVPZwSKaSmMxbhmS',
    'Accept': 'application/json'
}

print('Polling for new deploy...')
for i in range(30):
    url = 'https://api.render.com/v1/services/' + svc_id + '/deploys?limit=3'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        for item in result:
            d = item.get('deploy', {})
            did = d.get('id', '')
            status = d.get('status', '')
            created = d.get('createdAt', '')[:19]
            print('  ID:', did, '| Status:', status, '| Created:', created)
        latest = result[0].get('deploy', {})
        status = latest.get('status', '')
        if status in ['live', 'build_failed', 'update_failed', 'canceled']:
            if status == 'live':
                print('\nDEPLOYED! Live at: https://intrusion-detection-pssr.onrender.com')
            else:
                print('\nDeploy status:', status)
            break
        print('--- [' + str(i+1) + '/30] waiting 20s ---')
    time.sleep(20)
