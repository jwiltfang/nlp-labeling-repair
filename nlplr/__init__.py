"""
The purpose of this program is data cleaning in order to improve data analysis of event logs
"""
import logging

logger = logging.getLogger(__name__)
if not logger.hasHandlers():  # To ensure reload() doesn't add another one
    file_formatter = logging.Formatter('%(asctime)s : %(levelname)s - %(module)s %(funcName)10s :  %(message)s')
    stream_formatter = logging.Formatter('%(levelname)s - %(module)s %(funcName)10s :  %(message)s')

    log_stream = logging.StreamHandler()
    log_stream.setLevel(logging.DEBUG)
    log_stream.setFormatter(stream_formatter)

    log_file = logging.FileHandler(filename=r'log_file.log', mode='a')
    log_file.setLevel(logging.DEBUG)
    log_file.setFormatter(file_formatter)

    logger.addHandler(log_stream)
    # logger.addHandler(log_file)  # TODO reactivate
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.disabled = False
else:
    print('no logger acquired')
    print(logger.handlers)

logger.info(f'Configuration of logging handlers completed')