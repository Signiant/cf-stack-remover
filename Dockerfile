#FROM jfloff/alpine-python:3.4-slim
FROM python:3.7.1-alpine

MAINTAINER Signiant DevOps <devops@signiant.com>

COPY cf_delete_stacks.py /cf_delete_stacks.py
COPY run_cf_stack_remover.sh /run_cf_stack_remover.sh

RUN pip install boto3
# RUN chmod a+x /ecs_cluster_scaledown.py

#ENTRYPOINT ["python", "/cf_delete_stacks.py"]
ENTRYPOINT ["sh", "/run_cf_stack_remover.sh"]

CMD ["--help"]

