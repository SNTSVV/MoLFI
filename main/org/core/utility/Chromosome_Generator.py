import pandas as pd
import random
import re
from random import randint
from typing import List

from numpy.core.defchararray import startswith
from main.org.core.chromosome.chromosome import Chromosome
from main.org.core.chromosome.template import Template
from main.org.core.utility.log_message_adaptation import adapt_log_message
from main.org.core.utility.match_utility import compute_matched_lines
from main.org.core.utility.message import Message
from main.org.core.utility.log_file_reader import load_logs_into_df


class ChromosomeGenerator:
    """ This utility class is used to generate random chromosomes
    starting from the messages in the log file under analysis
    """

    def __init__(self, path: str, log_format: str, regex: List[str]):
        """ Constructor that takes the path to the log file as input
        and saves the content of the file as a list of strings
        each item in the list correspond to a line in the log file
        :param path: path to log file
        :param pattern: log line pattern (e.g., <date> <message>)
        """
        self.messages = {}
        self.parse_messages(path, log_format, regex)

    """============================================================================"""

    def parse_messages(self, path: str, log_format: str, regex: List[str]):
        """ Constructor that takes the path to the log file as input
        and saves the content of the file as a list of strings
        each item in the list correspond to a line in the log file
        :param path: path to log file
        :param log_format: log format (e.g., <date> <message>)
        :param regex: list of regular expressions used to detect trivial values
        """
        # print("Starting parsing the log")
        logs_df = load_logs_into_df(log_format=log_format, log_files=[path])

        columns = set()
        for index, row in logs_df.iterrows():
            new_msg = adapt_log_message(row['message'], regex=regex)
            string = new_msg.to_string()
            if not columns.__contains__(string):
                self.load_log_message(new_msg)
                columns.add(string)

        # print("Finished parsing the log")

    """============================================================================"""

    def generate_random_template(self):
        ''' Randomly select a cluster with id X from messages
        :return: a template from the cluster X
        the template has a length = X
        '''
        cluster_id = random.choice(list(self.messages.keys()))
        print(cluster_id)
        rand_value = randint(0, len(self.messages[cluster_id]) - 1)
        return self.generate_template_from_line(rand_value)

    def generate_template_from_line(self, cluster_id: int, rand_value: int):
        """ Generates a Template from a cluster
        """
        template = self.messages[cluster_id][rand_value].words[:]

        if len(template) > 1:
            contains_star = False
            for word in template:
                if word == "#spec#":
                    contains_star = True
                    break

            if not contains_star:
                modifiable_indexes = list()
                for index in range(0, len(template)):
                    if not (startswith(template[index], "[") or
                                re.match("\B\W\Z", template[index])):
                        modifiable_indexes.append(index)

                if len(modifiable_indexes) > 0:
                    index = random.choice(modifiable_indexes)
                    template[index] = '*'

        t = Template(template)
        compute_matched_lines(self.messages, t)
        return t

    """============================================================================"""

    def generate_100cov_chromosome(self):
        '''Create a chromosome with 100 coverage for each cluster
        the created chromosome shuold have the same keys as the messages
         of the chromosome generator and for each key, values (templates) must cover
         all messages in that cluster
        :return: chromosome
        '''
        chromosome = Chromosome({})
        for key in self.messages.keys():
            if key == 0:
                continue
            uncovered_lines = list(range(0, len(self.messages[key])))
            while len(uncovered_lines) > 0:
                message_index = random.choice(uncovered_lines)
                template = self.generate_template_from_line(key, message_index)
                chromosome.add_template(template)
                compute_matched_lines(self.messages, template)
                for line in template.matched_lines:
                    if uncovered_lines.__contains__(line):
                        uncovered_lines.remove(line)
        # print("Created one Chromosome")
        return chromosome

    def load_log_message(self, message: Message):
        """ Adds a log message to messages
        :param message: an object of type Message
        :return: the attribute messages with an additional element
        """
        key = message.get_length()
        if key in self.messages:
            self.messages[key].append(message)
        else:
            self.messages[key] = []
            self.messages[key].append(message)
