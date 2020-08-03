from downalod_manager import docker_client
from datetime import datetime
from downalod_manager.log_data_collector import log_data_from_text


def get_containers_data():
    client = docker_client.get_client()
    containers = client.containers.list()
    container_datas = {}
    for container in containers:
        if is_scraper_container(container):
            log_data = get_log_data_from_container(container)
            container_datas[container.name] = log_data
            container_datas[container.name]["age"] = container_age(container)
    client.close()
    return container_datas


def is_scraper_container(container):
    return "scraper" in container.name


def get_log_data_from_container(container):
    log = container.logs().decode("utf-8")
    log_tail = log.split("\n")[-100:]
    log_data = log_data_from_text(log_tail)
    return log_data


def container_age(container):
    started_str = container.attrs["State"]["StartedAt"].replace("T", " ").split(".")[0]
    started = datetime.strptime(started_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.utcnow()
    age = now - started
    age_in_minute = int(age.total_seconds() / 60)
    return age_in_minute

# gather_log_data_from_contaners()
# stop_scraper()