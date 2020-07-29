import docker
import config

client = None


def get_client():
    global client
    if config.docker_host != "-" and client is None:
        client = docker.DockerClient(base_url=config.docker_host, tls=False)
    elif client is None:
        client = docker.from_env()
    return client

