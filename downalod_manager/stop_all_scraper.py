import docker


def stop_all_scraper():
    client = docker.DockerClient(base_url="tcp://192.168.0.70:2375", tls=False)
    containers = client.containers.list()
    container_datas = {}
    for container in containers:
        if is_scraper_container(container):
            container.stop()


def is_scraper_container(container):
    return "scraper" in container.name


stop_all_scraper()