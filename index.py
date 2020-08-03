from data_inserter.data_inspector import data_explorer
from data_inserter import scraped_data_into_row
from data_inserter import read_json_data_from_file

# read_json_data_from_file.read_containers_output(scraped_data_into_row.response_to_tuple)
# data_inspector.write_result_to_file()

# from tools import config
# from tools.logger import get_logger, setup_logger
# from apscheduler.schedulers.blocking import BlockingScheduler
# from downalod_manager.download_job_manager import manage_download_execution

# setup_logger()
# logger = get_logger()
# logger.debug("")
# logger.debug("execution started: ")
# search_params = config.seach_params.copy()
# scheduler = BlockingScheduler()
# job = scheduler.add_job(manage_download_execution, 'interval', args=[search_params], minutes=1, name="scraper_manager")
# scheduler.start()
