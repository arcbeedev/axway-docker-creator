# axway-docker-creator



Build the base image:
./build_base_image.py --installer=APIGateway_7.7.20211130_Install_linux-x86-64_BN02.run --os=centos7

 Admin Node Manager (ANM) image:
./build_anm_image.py --default-cert --default-user --license=license.lic


Build the API Gateway (APIGW) and API Manager (APIM) image:
./build_gw_image.py --license=lic.lic --merge-dir tmp/apigateway --default-cert --group-id=defaultgroup  --api-manager 


Build the API Gateway (APIGW) and API Manager (APIM) image: without --api-manager  and with fed
./build_gw_image.py --license=lic.lic --merge-dir tmp/apigateway --default-cert --fed=tmp/fed.fed --group-id=defaultgroup  


Confirm your Docker images have been built:
docker images

Start:
docker create network api-gateway-domain
docker run --name=admin-node-manager --publish 8090:8090 --network=api-gateway-domain admin-node-manager 
 
docker run -p 8075:8075 -p 8065:8065 -p 8080:8080 --network=api-gateway-domain -e CASS_PASS=cassandra123 -e CASS_USERNAME=cassandra -e CASS_HOST=172.16.195.147 -e EMT_ANM_HOSTS="admin-node-manager:8090" api-gateway-defaultgroup  


 #add pass
                cass_config_db = es.get("/[CassandraSettings]name=Cassandra Settings")
                cass_config_db.setStringField("username", "${environment.CASS_USERNAME}")
                #cass_config_db.setStringField("password", "Y2Fzc2FuZHJh") #cassandra
                cass_config_db.setStringField("password", "Y2Fzc2FuZHJhMTIz") #cassandra123
                es.updateEntity(cass_config_db);
