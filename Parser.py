import re


MSG_LENGTH = 100


class Parser:

    """Default regular expression in case no file with a pattern is provided"""
    DEFAULT_REGEX_FORMAT = r'(?P<date>\d+/\d{2}/\d{2}) (?P<timestamp>([0-1]+\d|2[0-3]):[0-5]\d:[0-5]\d) (?P<pid>\[\d+\]) (?P<description>.*)'

    def __init__(self, pattern_file=None):
        """
        The Parser object will define how to parse a string

        :param pattern_file: Path to the pattern file
        """
        self.pattern_file = pattern_file
        self.pattern = self.DEFAULT_REGEX_FORMAT if pattern_file is None else self.__extract_pattern()

    def __extract_pattern(self):
        """
        Extracting a pattern in case a file is provided with a pattern of interest,
        said pattern should be defined in the first line of the file

        :return:
        first_line (str): First line of the file defining the pattern in the first line
        DEFAULT_REGEX_FORMAT (str): Default regular expression in case when reading the provided file it throws an exception
        """
        try:
            with open(self.pattern_file) as f:
                first_line = f.readline().strip()
                if first_line and len(first_line) > 0:
                    return first_line
                else:
                    print(f"{'-' * MSG_LENGTH} \n The first line of the file might not be well formatted, the default log format will be employed \n{'-' * MSG_LENGTH}")
                    return self.DEFAULT_REGEX_FORMAT
        except Exception as e:
            print(f"{'-' * MSG_LENGTH} \n Error while reading file, the default log format will be employed \n{'-' * MSG_LENGTH}")
            print(f"{'-' * MSG_LENGTH}\n {e} \n{'-' * MSG_LENGTH}")
            return self.DEFAULT_REGEX_FORMAT

    def parse_log(self, log):
        """
        Parsing a log given the pattern provided when initializing a Parser

        :param log: log line
        :return: dictionary with the group names as keys and the matched string as the value for that key given the provided pattern
        """
        m = re.match(self.pattern, log)
        return m.groupdict()
