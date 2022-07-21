FROM ubuntu:latest

# Update and install dependencies
RUN apt-get update && apt-get install -y cron rsync python3 python3-pip
RUN pip3 install prometheus-client

# Create directories
RUN mkdir -p /usr/src/app/rsync_exporter
RUN mkdir -p /usr/src/app/rsync_exporter/exercise_root
RUN mkdir -p /usr/src/app/rsync_exporter/tmp

# define working directory
WORKDIR /usr/src/app/rsync_exporter

# Copying files
# Source code
COPY main.py Exporter.py Parser.py test.py /usr/src/app/rsync_exporter/
# Default format log
COPY format.txt /usr/src/app/rsync_exporter
# Rsync configuration and init log file
COPY rsync.log rsyncd_example.conf /usr/src/app/rsync_exporter/
# Rsync starting scripts & cron config
COPY start_rsync_pipeline.sh generate_logs.sh /usr/src/app/rsync_exporter/
COPY cron_task /etc/cron.d/cron_task
# Toy image
COPY utah_teapot.png /usr/src/app/rsync_exporter/exercise_root

# Execution permission
RUN chmod +x start_rsync_pipeline.sh
RUN chmod +x generate_logs.sh
RUN chmod +x /etc/cron.d/cron_task

# Cronjob into the cron table
RUN crontab /etc/cron.d/cron_task

# Exposing port
EXPOSE 8080

ENTRYPOINT [ "./start_rsync_pipeline.sh"]