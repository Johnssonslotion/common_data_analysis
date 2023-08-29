### default celery worker with mq enabled
FROM celeryworker:base

## for test, transfer from dev to prod
### copy code

RUN mkdir -p /home/worker/geospatial_data_analysis/app
RUN mkdir -p /home/worker/geospatial_data_analysis/tests
RUN mkdir -p /home/worker/geospatial_data_analysis/app/api
RUN mkdir -p /home/worker/geospatial_data_analysis/app/base
RUN mkdir -p /home/worker/geospatial_data_analysis/app/model
RUN mkdir -p /home/worker/geospatial_data_analysis/app/utils
RUN mkdir -p /home/worker/geospatial_data_analysis/tests/module_test
RUN mkdir -p /home/worker/geospatial_data_analysis/tests/unit_test

COPY ./app /home/worker/geospatial_data_analysis/app
COPY ./tests /home/worker/geospatial_data_analysis/tests


USER root
RUN chown -R worker:root /home/worker && chmod -R 775 /home/worker
COPY ./entrypoint.sh /home/worker/geospatial_data_analysis/entrypoint.sh
RUN chmod +x /home/worker/geospatial_data_analysis/entrypoint.sh
WORKDIR /home/worker/geospatial_data_analysis
USER worker
COPY ./pyproject.toml /home/worker/geospatial_data_analysis/pyproject.toml
RUN poetry update
ENTRYPOINT ["entrypoint.sh"]