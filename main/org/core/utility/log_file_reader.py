import pandas as pd
import re
import os

import logging
logger = logging.getLogger(__name__)


def log_file_reader(logpath):

    with open(logpath) as f_read:
        lines = f_read.readlines()

    return lines


def load_logs_into_df(log_format: str, log_files: list):
    """
    Load logs with parsing according to the given log format.
    :param log_format:
    :param log_files:
    :return:
    """
    header, pattern = generate_pattern_from_log_format(log_format)
    if 'message' not in header:
        print(f'ERROR: <message> is not in log_format={log_format}')
        exit(-1)

    log_id = 1
    log_dfs = []
    for file in log_files:
        log_lines = []
        with open(file, 'r', errors='replace') as log:
            for line in log:
                m = re.match(pattern, line.strip())
                if m:
                    log_line = [m.group(h) for h in header]
                    log_lines.append(log_line)
                else:
                    logger.debug(f'Skip non-matched log_line={line.strip()}')
        log_df = pd.DataFrame(log_lines, columns=header)
        log_df.insert(0, 'lineID', None)
        log_df['lineID'] = [i + 1 for i in range(len(log_lines))]
        log_df.insert(0, 'logID', log_id)
        log_id += 1
        log_dfs.append(log_df)
        logger.info(f'loaded log file (lines=%d): %s' % (len(log_lines), file))

    logs_df = pd.concat(log_dfs, ignore_index=True)
    print(f'Total number of log messages in raw logs: %d' % len(logs_df))

    return logs_df


def generate_pattern_from_log_format(log_format: str):
    header = re.findall(r'<(\S+?)>', log_format)
    pattern = re.sub(r'(<\S+?>)', r'(?P\1.+?)', log_format)
    pattern = re.sub(r'<(\S+)_ext>\.\+\?', r'<\1_ext>.+', pattern)
    pattern = re.sub(r'\s+', r'\\s+', pattern)
    pattern = '^' + pattern + '$'
    return header, pattern
