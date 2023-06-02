import docker

# create a Docker client instance
client = docker.from_env()

# retrieve a list of all running containers
containers = client.containers.list()

# iterate over each container and print its name and defined ports
for container in containers:
    ports = container.attrs['Config']['ExposedPorts']
    print("Container name:", container.name)
    print("Defined ports:")
    for port in ports:
        print(" -", port)

cts = client.containers.list()
print (cts)
