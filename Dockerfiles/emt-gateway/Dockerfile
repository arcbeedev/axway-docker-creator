ARG PARENT_IMAGE
FROM $PARENT_IMAGE

ARG GROUP_ID
ARG DOCKER_IMAGE_ID
ARG SETUP_APIMGR
ARG FIPS_MODE

COPY opt/emt_resources /opt/emt
COPY scripts/* /opt/Axway/apigateway/posix/bin/ 

RUN cp /opt/emt/lic.lic /opt/Axway/apigateway/conf/licenses && \
    mkdir -p /opt/Axway/apigateway/groups/certs/private && \
    touch /opt/Axway/apigateway/groups/certs/index.txt && \
    echo $(printf '%x\n' `date +"%s%2N"`) > /opt/Axway/apigateway/groups/certs/serial && \
    cp /opt/emt/domaincert.pem /opt/Axway/apigateway/groups/certs/ && \
    cp /opt/emt/domainkey.pem /opt/Axway/apigateway/groups/certs/private/ && \
    cd /opt/Axway/apigateway/posix/bin && \
    ./setup-emt-instance \
        --props /opt/emt/config.props \
        --group-id "$GROUP_ID" \
        --fed /opt/emt/fed.fed \
        --pol /opt/emt/pol.pol \
        --env /opt/emt/env.env \
        --merge-dir /opt/emt/apigateway \
        --docker-image-id "$DOCKER_IMAGE_ID" \
        --setup-apimgr $SETUP_APIMGR \
        --fips $FIPS_MODE && \
    rm -rf /opt/emt && \
    chgrp -R 0 /opt/Axway && \
    chmod -R 770 /opt/Axway

EXPOSE 8089
EXPOSE 8080
EXPOSE 8065
EXPOSE 8075

CMD ["/opt/Axway/apigateway/posix/bin/start-emt-instance"]
