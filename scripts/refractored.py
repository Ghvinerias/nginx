import docker
import time
import http.client
import json
import os
import subprocess

# Create a Docker client
client = docker.from_env()
os.environ['NPM_USER'] = "admin@slick.ge"
os.environ['NPM_PSWD'] = "SLICK@dmin"

npmssl = os.environ.get('NPM_SSL', '1')
npmhost = os.environ.get('NPM_HOST', 'npmadmin.slick.ge')
npmport = os.environ.get('NPM_PORT', '443')


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

def get_bearer(conn):
    payload = {
        "identity": os.environ['NPM_USER'],
        "secret": os.environ['NPM_PSWD']
    }
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/tokens", json.dumps(payload), headers)
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
    payload = {
        "domain_names": [domain_names],
        "forward_host": forward_host,
        "forward_port": forward_port,
        "access_list_id": 0,
        "certificate_id": 8,
        "ssl_forced": ssl_forced,
        "caching_enabled": 0,
        "block_exploits": block_exploits,
        "advanced_config": "",
        "meta": {
            "letsencrypt_agree": False,
            "dns_challenge": False,
            "nginx_online": True,
            "nginx_err": None
        },
        "allow_websocket_upgrade": allow_websocket_upgrade,
        "http2_support": http2_support,
        "forward_scheme": forward_scheme,
        "enabled": 1,
        "locations": [],
        "hsts_enabled": hsts_enabled,
        "hsts_subdomains": hsts_subdomains
    }
    
    conn.request("POST", "/api/nginx/proxy-hosts", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    response = data.decode("utf-8")
    if "error" in json.loads(response):
        if json.loads(response)["error"]["message"] == f"{domain_names} is already in use":
            print(f"{domain_names} already exists")
        else:
            print("Something went wrong")
    else:
        print(f"Added configuration for {domain_names}")

    return response

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

conn = None


if npmssl == "1":
    conn = http.client.HTTPSConnection(npmhost, npmport) # type: ignore
else:
    conn = http.client.HTTPConnection(npmhost, npmport) # type: ignore

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
