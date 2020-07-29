import docker
import config
import time
import docker_data_collector
from datetime import datetime
from tools.logger import get_logger, setup_logger
from apscheduler.schedulers.blocking import BlockingScheduler


containers_started = []
containers_frozen = []


def manage_download_execution(search_params: list):
    global containers_started, containers_frozen

    logger.debug("\n")
    logger.debug("running manager: ")
    logger.debug("")
    client = docker.DockerClient(base_url="tcp://192.168.0.70:2375", tls=False)

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


def log_running_containers():
    global containers_started, containers_frozen
    containers_data = docker_data_collector.get_containers_data()
    logger.debug("running_cotainers:")
    for container_name, container_data in containers_data.items():
        logger.debug(f" \t{container_name} : {container_data}")

    logger.debug("containers started : " + str(containers_started))
    logger.debug("frozen containers: " + str(containers_frozen))


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


def some_job():
    logger.debug("test message")


setup_logger()
logger = get_logger()
logger.debug("")
logger.debug("execution started: ")
search_params = config.seach_params.copy()

manage_download_execution(search_params)

scheduler = BlockingScheduler()
job = scheduler.add_job(manage_download_execution, 'interval', args=[search_params], minutes=1, name="scraper_manager")
scheduler.start()