import services.file_service as file
import config as conf
import logging


def get_log_lines_by(log_err_type):
    log_data = file.read_file(conf.PATH_TO_LOG_FILE)
    filtered_log = []
    if len(log_data) > 0:
        for line in log_data:
            if log_err_type.upper() in line:
                filtered_log.append(line)
        return filtered_log
    return []


def clear_log(message='---- log after clear ----'):
    open(conf.PATH_TO_LOG_FILE, 'w').close()
    if message != '':
        logging.info(message)
