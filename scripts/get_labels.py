import socket
import os
ct_name = os.environ['HOSTNAME']

def get_docker_host_ip(ct_name):
    docker_host_ip = socket.gethostbyname(ct_name)
    return docker_host_ip

# Example usage
host_ip = get_docker_host_ip(ct_name)
print(host_ip)
