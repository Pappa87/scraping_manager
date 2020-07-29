import re
from datetime import datetime

number_of_lines_to_read = 100


def log_data_from_file(logfile_path):
    with open(logfile_path, encoding='utf-8') as log_file:
        log_tail = []
        for line in (log_file.readlines()[-number_of_lines_to_read:]):
            log_tail.append(line)
        data = log_data_from_text(log_tail)
        return data


def log_data_from_text(log_tail):
    try:
        duration_from_last_log = int((datetime.now() - get_last_log_time(log_tail)).total_seconds() / 60)
    except ValueError:
        return {"error": "cant calculate last log time"}

    result = {}
    result["duration_from_last_log"] = duration_from_last_log
    result.update(gather_article_job_data(log_tail))
    return result


def get_last_log_time(lines):
    for line in lines[::-1]:
        try:
            date_str = line.split("|")[0]
            date = datetime.strptime(date_str, "%Y.%m.%d. %H:%M:%S ")
            return date
        except Exception as e:
            pass
    raise ValueError


def gather_article_job_data(lines) -> dict:
    result = {}
    result["total_data"] = total_number_of_jobs(lines)
    result["remain"] = remaining_number_of_jobs(lines)
    result["succesfull"] = succesfully_scraped_jobs_number(lines)
    result["failed"] = failed_scraped_jobs_number(lines)
    return result


def total_number_of_jobs(lines):
    filtered_lines = list(filter(lambda line: line.endswith("job remained"), lines))
    if len(filtered_lines) == 0: return "-"
    last_line = filtered_lines[-1]
    regex_match = re.search("\d*/\d*", last_line).group(0)
    total_jobs = regex_match.split("/")[1]
    return total_jobs


def remaining_number_of_jobs(lines):
    filtered_lines = list(filter(lambda line: line.endswith("job remained"), lines))
    if len(filtered_lines) == 0: return "-"
    last_line = filtered_lines[-1]
    regex_match = re.search("\d*/\d*", last_line).group(0)
    remain = regex_match.split("/")[0]
    return remain


def succesfully_scraped_jobs_number(lines):
    filtered_lines = list(filter(lambda line: "number of successful scraping" in line, lines))
    if len(filtered_lines) == 0: return "-"
    last_line = filtered_lines[-1]
    number_of_succefull_srape = re.search("\d*$", last_line).group(0)
    return number_of_succefull_srape


def failed_scraped_jobs_number(lines):
    filtered_lines = list(filter(lambda line: "number of failed scraping" in line, lines))
    if len(filtered_lines) == 0: return "-"
    last_line = filtered_lines[-1]
    number_of_failed_srape = re.search("\d*$", last_line).group(0)
    return number_of_failed_srape


# logfile_path = r"C:\tmp\scheduler_log.txt"
# data = log_data_from_file(logfile_path)
# print(data)
