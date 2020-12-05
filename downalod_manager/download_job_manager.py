from tools import config
import time
from downalod_manager import docker_data_collector, docker_client
from tools.logger import get_logger, setup_logger

logger = get_logger()
containers_started = []
containers_frozen = []


def manage_download_execution(search_params):
    global containers_started, containers_frozen

    logger.debug("\n")
    logger.debug("running manager: ")
    logger.debug("docker config: " + config.docker_host)
    logger.debug("")
    client = docker_client.get_client()

    containers_data = docker_data_collector.get_containers_data()

    # stops frozen container
    for container_name, container_data in containers_data.items():
        if container_data["duration_from_last_log"] > 10:
            frozen_container = client.containers.get(container_name)
            frozen_container.stop()
            frozen_container.remove()
            containers_frozen.append(container_name)
            logger.debug(f"{container_name} container frozed, and stopped, and removed")

    # deploy a container if can
    if containers_deployable(search_params):
        search_param = search_params.pop()
        search_exp = search_param["search_exp"]
        container_name = f'scraper_{search_param["name"]}'

        run_scraper(client, search_exp, container_name)
        containers_started.append(container_name)
        logger.debug(f"container started with search exp: {search_param['search_exp']}")
    logger.debug("")

    client.close()
    log_running_containers()


def containers_deployable(search_params):
    containers_data = docker_data_collector.get_containers_data()
    return len(containers_data) < config.maximum_parallelr_scraper and len(search_params) != 0


def run_scraper(client, search_exp, name):
    image = "scraper"
    name = name
    command = """bash -c "bash webRTC_blocker.sh && node index.js" """
    environment = {"SEARCH_EXP": search_exp}
    cap_add = ["NET_ADMIN"]
    volumes = {f"/scrapers_output/{name}/scraper_output": {'bind': '/scraper_output', 'mode': 'rw'}}
    network = "scraperv2_scraper-network"
    if has_container(client, name):
        client.containers.get(name).stop()
        client.containers.get(name).remove()
    client.containers.run\
    (
        image=image,
        name=name,
        command=command,
        environment=environment,
        cap_add=cap_add,
        volumes=volumes,
        network=network,
        detach=True
    )
    time.sleep(30)


def has_container(client, name):
    container_list = client.containers.list(all=True)
    container_name_list = list(map(lambda x: x.name, container_list))
    return name in container_name_list


def log_running_containers():
    global containers_started, containers_frozen
    containers_data = docker_data_collector.get_containers_data()
    logger.debug("running_cotainers:")
    for container_name, container_data in containers_data.items():
        logger.debug(f" \t{container_name} : {container_data}")

    logger.debug(f"number containers started : {len(containers_started)}\\{len(config.seach_params)}")
    logger.debug("frozen containers: " + str(containers_frozen))

