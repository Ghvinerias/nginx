import http.client
import json



def get_bearer():
    conn = http.client.HTTPConnection("app", 81)
    payload = json.dumps({
      "identity": "admin@example.co",
      "secret": "asdASD123"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/tokens", payload, headers)
    res = conn.getresponse()
    response_json = json.loads(res.read().decode("utf-8"))
    token = response_json["token"]
    headers['Authorization'] = f'Bearer {token}'
    return headers
  
headers = get_bearer()


conn = http.client.HTTPConnection("app", 81)
payload = ''
conn.request("GET", "/api/nginx/proxy-hosts", payload, headers)
res = conn.getresponse()
data = res.read()
got_hosts = data.decode("utf-8")
print(got_hosts)



domain_names = "whoami5.test"
forward_host = "whoami5"
forward_port = 2005
ssl_forced = 0
block_exploits = 1
allow_websocket_upgrade = 0
http2_support = 0
forward_scheme = "http"
hsts_enabled = 0
hsts_subdomains = 0


payload = """{{
    "domain_names": [
        "{}"
    ],
    "forward_host": "{}",
    "forward_port": {},
    "access_list_id": 0,
    "certificate_id": 0,
    "ssl_forced": {},
    "caching_enabled": 0,
    "block_exploits": {},
    "advanced_config": "",
    "meta": {{
        "letsencrypt_agree": false,
        "dns_challenge": false,
        "nginx_online": true,
        "nginx_err": null
    }},
    "allow_websocket_upgrade": {},
    "http2_support": {},
    "forward_scheme": "{}",
    "enabled": 1,
    "locations": [],
    "hsts_enabled": {},
    "hsts_subdomains": {}
}}""".format(domain_names, forward_host, forward_port, ssl_forced, block_exploits, allow_websocket_upgrade, http2_support, forward_scheme, hsts_enabled, hsts_subdomains)



conn = http.client.HTTPConnection("app", 81)
conn.request("POST", "/api/nginx/proxy-hosts", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))



