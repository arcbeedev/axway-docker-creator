ARG PARENT_IMAGE
FROM $PARENT_IMAGE

ARG DOCKER_IMAGE_ID
ARG ANM_USERNAME
ARG HEALTHCHECK
ARG METRICS_DB_URL
ARG METRICS_DB_USERNAME
ARG FIPS_MODE

COPY  opt/emt_resources /opt/emt
COPY  scripts/* /opt/Axway/apigateway/posix/bin/

RUN if [ -e /opt/emt/lic.lic ]; then cp /opt/emt/lic.lic /opt/Axway/apigateway/conf/licenses; fi && \
    if [ "$HEALTHCHECK" = "True" ]; then cp /opt/emt/anm_hc_path.xml /opt/Axway/apigateway/samples/SamplePolicies/HealthCheck; fi && \
    mkdir -p /opt/Axway/apigateway/groups/certs/private && \
    touch /opt/Axway/apigateway/groups/certs/index.txt && \
    echo $(printf '%x\n' `date +"%s%2N"`) > /opt/Axway/apigateway/groups/certs/serial && \
    cp /opt/emt/domaincert.pem /opt/Axway/apigateway/groups/certs/ && \
    cp /opt/emt/domainkey.pem /opt/Axway/apigateway/groups/certs/private/ && \
    cd /opt/Axway/apigateway/posix/bin && \
    ./setup-emt-nodemanager \
        --props /opt/emt/config.props \
        --fed /opt/emt/fed.fed \
        --anm-username "$ANM_USERNAME" \
        --merge-dir /opt/emt/apigateway \
        --healthcheck $HEALTHCHECK \
        --docker-image-id "$DOCKER_IMAGE_ID" \
        --metrics-db-url "$METRICS_DB_URL" \
        --metrics-db-username "$METRICS_DB_USERNAME" \
        --fips $FIPS_MODE && \
    rm -rf /opt/emt && \
    chgrp -R 0 /opt/Axway && \
    chmod -R 770 /opt/Axway

EXPOSE 8090

CMD ["/opt/Axway/apigateway/posix/bin/start-emt-nodemanager"]
