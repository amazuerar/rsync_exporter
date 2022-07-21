import re
import os
import time

from prometheus_client import start_http_server, Counter
from Parser import Parser


MSG_LENGTH = 100


class Exporter:

    def __init__(self, file_path, pattern, seconds=1, port=8080):
        """
        The Exporter object will export various statistics about new content (i.e., new log) given a log file in a way that can be scraped by Prometheus

        :param file_path: Path to the log file
        :param pattern: Path to the pattern file
        :param seconds: Time in seconds to check for new content in the log file. Default value is 1
        :param port: Port in which one starts a WSGI server for prometheus metrics. Default value is 8080
        """
        self.file_path = file_path
        self.pattern = pattern
        self.seconds = seconds
        self.port = port

    def collect_metrics(self):
        """
        Define metric types to be collected and record said metrics
        """

        connections = Counter("rsync_connections_total", "Total number of connections made to rsync daemon")
        executions = Counter("rsync_executions_total", "Total number of rsync executions made")
        serv_error = Counter("rsync_service_error_total", "Total number of Service errors by status code", ["status_code"])
        bytes_recv = Counter("rsync_data_received_bytes_total", "Total bytes received from rsync")
        bytes_sent = Counter("rsync_data_sent_bytes_total", "Total bytes sent from rsync")
        bytes_total = Counter("rsync_exchange_data_bytes_total", "Total bytes exchange from rsync")

        print(f"{'*' * MSG_LENGTH} \n Starting server for Prometheus metrics, port: {self.port} \n{'*' * MSG_LENGTH}")

        start_http_server(self.port)

        def record_metric(incoming_line):
            """
            Increases metrics given an amount and record such a value

            :param incoming_line: new line coming from the living log file,
            it has a dictionary structure, in order to analyze this new log
            one is interested in the value given the key 'description'
            """

            line_log = incoming_line['description']

            if "connect" in line_log:
                connections.inc()
            elif "rsync on" in line_log:
                executions.inc()
            elif "rsync error" in line_log:
                code_regex = r'\(code [1-9]?[0-9]\)'
                match = re.search(code_regex, line_log)
                status_code = match.group(0)
                serv_error.labels(status_code=status_code).inc()
            elif "total size" in line_log:

                byte_regex = r'(?P<sent>sent \d+ bytes)  (?P<received>received \d+ bytes)  (?P<total>total size \d+)'
                match = re.match(byte_regex, line_log)

                sent = int(''.join(filter(lambda x: x.isdigit(), match.group('sent'))))
                rec = int(''.join(filter(lambda x: x.isdigit(), match.group('received'))))
                total = int(''.join(filter(lambda x: x.isdigit(), match.group('total'))))

                bytes_sent.inc(sent)
                bytes_recv.inc(rec)
                bytes_total.inc(total)

            else:
                pass

        """Defining a new Parser given the provided pattern"""
        p = Parser(self.pattern)

        """Analyzing each new line in the living log file and it is parsed"""
        for line in self.read_living_log_file():
            par_line = p.parse_log(line)
            try:
                record_metric(par_line)
            except Exception as e:
                print(f"{'-' * MSG_LENGTH}\nError while extracting metrics regarding log:{line}\n{'-' * MSG_LENGTH}")
                print(f"{'-' * MSG_LENGTH}\n {e} \n{'-' * MSG_LENGTH}")
                continue

    def read_living_log_file(self):
        """
        Allows to check if the log file has new line.
        In case there is no new line, it will check again in {self.seconds}
        In case there is new line, it will yield the line

        :return: curr_line: The string regarding the new line in the log file
        """

        with open(self.file_path, "r") as log_file:
            log_file.seek(0, os.SEEK_END)
            while True:
                curr_pos = log_file.tell()
                curr_line = log_file.readline()
                if not curr_line:
                    log_file.seek(curr_pos)
                    time.sleep(self.seconds)
                else:
                    yield curr_line
