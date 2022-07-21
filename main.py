import argparse
import os
from Exporter import Exporter


MSG_LENGTH = 100


def main():

    print(f"{'*' * MSG_LENGTH} \n Starting Rsyncd logfile exporter \n{'*' * MSG_LENGTH}")

    parser = argparse.ArgumentParser(description='Rsync logfile exporter & analyzer')
    parser.add_argument('-p', '--path_log_file', metavar='PATH_TO_LOG_FILE', required=True, help='Path to the log file of interest')
    parser.add_argument('-f', '--path_log_format', metavar='PATH_TO_LOG_FORMAT', required=False, help='Path to the file defining the regular expression describing the format of a log')
    parser.add_argument('-s', '--seconds', required=False, help='Time in seconds in order to examine the log file looking for new content, must be an integer. Default value is 1', type=int, default=1)
    parser.add_argument('-x', '--port', metavar='PROMETHEUS_PORT', required=False, help='Port employed in order to expose metrics. Default value is 8080', type=int, default=8080)
    args = parser.parse_args()

    def is_valid_file(path):
        """
        Verifies whether a path is a valid path file or not
        :param path: path to a file
        :return: Boolean verifying whether a path is a valid path file or not
        """
        return os.path.isfile(path)

    try:
        if is_valid_file(args.path_log_file):
            if args.path_log_format is not None:
                if is_valid_file(args.path_log_format):
                    exporter = Exporter(args.path_log_file, args.path_log_format, args.seconds, args.port)
                    exporter.collect_metrics()
                else:
                    print(f"{'-' * MSG_LENGTH} \n Error while reading file in PATH_TO_LOG_FORMAT, the path is not valid \n{'-' * MSG_LENGTH}")
            else:
                exporter = Exporter(args.path_log_file, None, args.seconds, args.port)
                exporter.collect_metrics()
        else:
            print(f"{'-' * MSG_LENGTH} \n Error while reading log file in PATH_TO_LOG_FILE, the path is not valid \n{'-' * MSG_LENGTH}")
    except Exception as e:
        print(f"{'-' * MSG_LENGTH} \n Error while executing the analysis \n{'-' * MSG_LENGTH}")
        print(f"{'-' * MSG_LENGTH} \n {e} \n{'-' * MSG_LENGTH}")


if __name__ == '__main__':
    main()
