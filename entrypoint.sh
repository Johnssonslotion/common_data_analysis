#!/bin/bash
source .venv/bin/activate
echo "RABBITMQ_WORKER_USER: $RABBITMQ_WORKER_USER"
echo "RABBITMQ_WORKER_PASS: $RABBITMQ_WORKER_PASS_ENC"
echo "ENV : $ENV"
python ./app/celery_main.py