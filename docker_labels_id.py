import docker
import sys

def print_container_labels(container_id):
    client = docker.DockerClient(base_url='tcp://infra-01.slick.ge:2375')
    try:
        container = client.containers.get(container_id)
        labels = container.labels
        print(f"Container ID: {container.short_id}")
        if labels:
            print("Labels:")
            for key, value in labels.items():
                print(f"{key}: {value}")
        else:
            print("No labels found for the container.")
    except docker.errors.NotFound:
        print(f"Container with ID '{container_id}' not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the container ID as a command-line argument.")
    else:
        container_id = sys.argv[1]
        print_container_labels(container_id)
