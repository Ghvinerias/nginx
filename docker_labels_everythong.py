import docker

def print_labels_starting_with_slick():
    client = docker.DockerClient(base_url='tcp://infra-01.slick.ge:2375')
    containers = client.containers.list(all=True)

    for container in containers:
        container_id = container.short_id
        labels = container.attrs['Config']['Labels']
        
        print(f"Container ID: {container_id}")
        
        if labels:
            print("Labels starting with 'slick':")
            slick_labels = {key: value for key, value in labels.items() if key.startswith('slick')}
            if slick_labels:
                for key, value in slick_labels.items():
                    print(f"{key}: {value}")
            else:
                print("No 'slick' labels found for the container.")
        else:
            print("No labels found for the container.")
        print()

if __name__ == "__main__":
    print_labels_starting_with_slick()