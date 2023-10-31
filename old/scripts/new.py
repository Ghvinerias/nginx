import http.client
import json
import os
import subprocess

def get_docker_host_ip():
    command = "ip -4 addr show $(ip route show default | awk '/default/ {print $5}') | grep -oP '(?<=inet\s)\d+(\.\d+){3}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    docker_host_ip = output.decode().strip()
    return docker_host_ip


os.environ['NPM_USER'] = "admin@slick.ge"
os.environ['NPM_PSWD'] = "SLICK@dmin"
os.environ['NPM_SSL'] = "1"
os.environ['NPM_HOST'] = "npmadmin.slick.ge"
os.environ['NPM_PORT'] = "443"


USER = os.environ['NPM_USER']
PSWD = os.environ['NPM_PSWD']
npmssl = os.environ['NPM_SSL']
npmhost = os.environ['NPM_HOST']
npmport = os.environ['NPM_PORT']



def get_bearer(conn):
    payload = """{{
          "identity": "{}",
          "secret": "{}"
    }}""".format(USER, PSWD)
    headers = {
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/tokens", payload, headers)
    res = conn.getresponse()
    response_json = json.loads(res.read().decode("utf-8"))
    token = response_json["token"]
    headers['Authorization'] = f'Bearer {token}'
    return headers

def get_hosts(conn, headers):
    payload = ''
    conn.request("GET", "/api/nginx/proxy-hosts", payload, headers)
    res = conn.getresponse()
    data = res.read()
    got_hosts = data.decode("utf-8")
    return got_hosts

def add_host(domain_names, forward_host, forward_port, ssl_forced, block_exploits, allow_websocket_upgrade, http2_support, forward_scheme, hsts_enabled, hsts_subdomains, conn, headers):
    payload = """{{
        "domain_names": [
            "{}"
        ],
        "forward_host": "{}",
        "forward_port": {},
        "access_list_id": 0,
        "certificate_id": 8,
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
    
    conn.request("POST", "/api/nginx/proxy-hosts", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response = data.decode("utf-8")
    return response

conn = None

if npmssl == "1":
    conn = http.client.HTTPSConnection(npmhost, npmport) # type: ignore
else:
    conn = http.client.HTTPConnection(npmhost, npmport) # type: ignore





domain_names = "whoami8.test"
forward_port = 2001
ssl_forced = 0
block_exploits = 1
allow_websocket_upgrade = 0
http2_support = 0
forward_scheme = "http"
hsts_enabled = 0
hsts_subdomains = 0


forward_host = get_docker_host_ip()
headers = get_bearer(conn)
response = add_host(domain_names, forward_host, forward_port, ssl_forced, block_exploits, allow_websocket_upgrade, http2_support, forward_scheme, hsts_enabled, hsts_subdomains, conn, headers)
#print(response)





# Check if the response contains the "error" key
if "error" in json.loads(response):
    if json.loads(response)["error"]["message"] == f"{domain_names} is already in use":
        print(f"{domain_names} already exists")
    else:
        print("Something went wrong")
else:
    print(f"Added configuration for {domain_names}")

