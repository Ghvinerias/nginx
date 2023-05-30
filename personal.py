import docker
infra_01 = docker.DockerClient(base_url='tcp://infra-01.slick.ge:2375')
infra_02 = docker.DockerClient(base_url='tcp://infra-02.slick.ge:2375')
infra_03 = docker.DockerClient(base_url='tcp://infra-03.slick.ge:2375')


print({infra_01.containers.get("048f4008c5").labels["slick.dns"]})
print({infra_01.containers.get("048f4008c5").labels["slick.ssl"]})
print({infra_01.containers.get("048f4008c5").labels["slick.websock"]})

