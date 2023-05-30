import docker
import time

def listen_for_new_containers():
    client = docker.DockerClient(base_url='tcp://infra-01.slick.ge:2375')
    containers = client.containers.list()

    # Get the initial list of containers
    container_ids = set([container.id for container in containers])

    while True:
        time.sleep(5)  # Sleep for 5 seconds between checks
        containers = client.containers.list()

        # Get the updated list of containers
        updated_container_ids = set([container.id for container in containers])

        # Find the newly started containers
        new_container_ids = updated_container_ids - container_ids

        # Print labels for new containers
        for container_id in new_container_ids:
            container = client.containers.get(container_id)
            labels = container.attrs['Config']['Labels']
            print(f"Container ID: {container.short_id}")
            if labels:
                print("Labels:")
                for key, value in labels.items():
                    print(f"{key}: {value}")
            else:
                print("No labels found for the container.")

        # Update the container_ids set
        container_ids = updated_container_ids

if __name__ == "__main__":
    listen_for_new_containers()
