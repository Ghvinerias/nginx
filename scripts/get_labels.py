import docker
import time

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
            print("Example Usage:")
            print(f"Domain Names: {domain_names}")
            print(f"Forward Port: {forward_port}")
            print(f"SSL Forced: {ssl_forced}")
            # ... and so on

    # Sleep for 1 second before checking again
    time.sleep(1)
