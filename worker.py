import docker
import time
import http.client
import json
import os
import subprocess

# Create a Docker client
client = docker.from_env()
# Set the labels to monitor
labels = [
    "npm.domain_names",
    "npm.forward_port",
    "npm.ssl_forced",
    "npm.block_exploits",
    "npm.allow_websocket_upgrade",
    "npm.http2_support",
    "npm.forward_scheme",
    "npm.hsts_enabled",
    "npm.hsts_subdomains"
]

def get_docker_host_ip():
    command = "ip -4 addr show $(ip route show default | awk '/default/ {print $5}') | grep -oP '(?<=inet\s)\d+(\.\d+){3}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    docker_host_ip = output.decode().strip()
    return docker_host_ip


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



# Initialize variables for label values
domain_names = None
forward_port = None
ssl_forced = None
block_exploits = None
allow_websocket_upgrade = None
http2_support = None
forward_scheme = None
hsts_enabled = None
hsts_subdomains = None

# Function to report label values
def report_labels(container):
    global domain_names, forward_port, ssl_forced, block_exploits, allow_websocket_upgrade
    global http2_support, forward_scheme, hsts_enabled, hsts_subdomains

    # Reset variables to None
    domain_names = None
    forward_port = None
    ssl_forced = None
    block_exploits = None
    allow_websocket_upgrade = None
    http2_support = None
    forward_scheme = None
    hsts_enabled = None
    hsts_subdomains = None

    print("New Container Detected:")
    for label in labels:
        value = container.labels.get(label)
        if value is not None:
            var_name = label.split(".")[1]
            globals()[var_name] = value
            print(f"{label}: {value}")
        else:
            print(f"{label}: Not set")

# Get a list of existing container IDs
existing_containers = set(container.id for container in client.containers.list())

# Loop indefinitely
while True:
    # Get a list of running containers
    containers = client.containers.list()

    # Check for new containers
    for container in containers:
        if container.id not in existing_containers:
            # Report labels for new container
            report_labels(container)
            # Add container ID to existing containers set
            existing_containers.add(container.id)

            # Use the label values outside the function
            forward_host = get_docker_host_ip()
            headers = get_bearer(conn)
            response = add_host(domain_names, forward_host, forward_port, ssl_forced, block_exploits, allow_websocket_upgrade, http2_support, forward_scheme, hsts_enabled, hsts_subdomains, conn, headers)
            print(response)
            # ... and so on

    # Sleep for 1 second before checking again
    time.sleep(1)


