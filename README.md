# axway-docker-creator

## Introduction
This is an example of a new installation in Docker Containers. This installation is suitable for a DEV environment.


## Set up Docker environment
Your system must meet the following prerequisites before you can run the scripts to build and deploy API Gateway in Docker containers.

### Set up your Docker environment
You must have the following installed on your local system:

- Docker CE version 18.06 or later on CentOS 7
- Python version 3.x or later
- OpenSSL version 1.1 or later


### Set up API Gateway Docker scripts
- API Gateway Linux installer from [Axway Support.](https://support.axway.com/en/)


### API Gateway licenses
You must have specific API Gateway licenses to run the following:

- API Gateway container
- Admin Node Manager or API Gateway container in Federal Information Processing Standard (FIPS) mode
- API Manager-enabled API Gateway container
- API Gateway Analytics container



### Domain SSL certificates
To secure the communications between the Admin Node Manager and API Gateways, you can use the gen_domain_cert.py script to generate a self-signed CA certificate for a domain, or a Certificate Signing Request (CSR) to be signed by an external Certificate Authority (CA).

> If you already have a domain certificate (for example, from another API Gateway installation) you can skip this section. You can specify your existing domain certificate (certificate and private key in .pem format) to the build_anm_image.py and build_gw_image.py scripts. You cannot use one domain certificate for both a container deployment and a classic deployment if they are running in parallel.

### Generate domain certificates script options

You must specify the following as options when using the gen_domain_cert.py script:

Domain identifier
Passphrase for the domain private key
This script also supports additional options when generating certificates. For example:

Specify a signing algorithm (SHA256, SHA384, or SHA512)
Generate a CSR
Specify custom values for the fields in the domain certificate (for example, organization)
For the latest script usage and options, run the script with no options, or with the -h option.

`./gen_domain_cert.py -h`
Generate a default certificate and key

The following example creates a certificate and private key using default values.

Do not use default options on production systems. The --default-cert option is provided only as a convenience for development environments.
cd emt_containers-<version>
```
 ./gen_domain_cert.py --default-cert
 ```
This example creates a default certificate and private key:

The certificate uses a domain identifier of DefaultDomain
The certificate and key are stored in the certs/DefaultDomain directory
The certificate uses a default passphrase
Generate a self-signed certificate and key

The following example creates a self-signed certificate and private key.

```
 ./gen_domain_cert.py --domain-id=mydomain --pass-file=/tmp/pass.txt
 ```
This example creates a self-signed certificate and private key:

The certificate uses a domain identifier of mydomain.
The certificate and key are stored in the certs/mydomain directory
The certificate uses a specified passphrase
Generate a CSR

The following example creates a certificate signing request (CSR).

You must send the generated CSR to a CA for signing.
When running the scripts to build Admin Node Manager or API Gateway images, specify the certificate and private key returned from the CA, and not the CSR.
cd emt_containers-<version>
```
 ./gen_domain_cert.py --domain-id=mydomain --pass-file=/tmp/pass.txt --out=csr --O=MyOrg
 ```
This example creates a CSR that:

Uses a domain identifier of mydomain
Is stored in the certs/mydomain directory
Uses a specified passphrase and organization




### Create Docker images
To create a base Docker image containing an operating system and an API Gateway installation, use the build_base_image.py script. This script builds a base API Gateway Docker image using an API Gateway 7.7 Linux installer and a Docker image based on a standard or custom CentOS7 or RHEL7 operating system image.

 #### Base image script options

You must specify the following as options when using the build_base_image.py script:

API Gateway 7.7 Linux installer
Operating system based on one of the following:
Standard CentOS7 Docker image downloaded from the public Docker registry
Standard RHEL7 Docker image downloaded from the Red Hat Docker registry
If you specify a custom CentOS7 or RHEL7-based OS Docker image, Docker first tries to find the custom image in the local registry, and then tries to download it from a remote registry
 
 #### Create a base image based on standard CentOS7
 
```
 ./build_base_image.py --installer=APIGateway.run --os=centos7
 ```
 > APIGateway.run is the downloaded installer from Axway
 
 
 #### Create an Admin Node Manager (ANM) Docker image
 ```
./build_anm_image.py --default-cert --default-user --license=license.lic
```
 > Do not use default options on production systems. The --default-cert and --default-user options are provided only as a convenience for development environments.
 
  #### Create an API Gateway Manager (APIMGR) Docker image using defaults
  ```
./build_gw_image.py --license=lic.lic --merge-dir tmp/apigateway --default-cert --group-id=defaultgroup  --api-manager 
  ```
  > Do not use default options on production systems. The --default-cert and --default-user options are provided only as a convenience for development environments.


  #### Before Start the Docker images
 for a local start your images, you may have to create a Docker network to enable the communication between the images.
   ```
 docker create network api-gateway-domain
   ```
 
 
  #### Start an Admin Node Manager (ANM) Docker image
 ```
 docker run --name=admin-node-manager --publish 8090:8090 --network=api-gateway-domain admin-node-manager 
 ```
 
  #### Start an API Gateway Manager (APIMGR) Docker image
 ```
 docker run -p 8075:8075 -p 8065:8065 -p 8080:8080 --network=api-gateway-domain -e CASS_USERNAME=CASS_USER -e CASS_HOST=CASSANDRA_HOST -e EMT_ANM_HOSTS=anm:8090 api-gateway-defaultgroup  
 ```
 
 This example performs the following:
- Binds the default traffic port 8080 of the container to port 8080 on the host machine, which enables you to test the API Gateway on your host machine.
- Sets the CASS_HOST environment variable with the Apache Cassandra host that is used to store the API Manager data.
- Uses an environment variable EMT_TRACE_LEVEL to set a trace level inside the container. In the above example a trace level switches from INFO to DEBUG level during container startup.
- Sets the EMT_ANM_HOSTS environment variable to anm:8090 in the container. This enables the API Gateway to communicate with the Admin Node Manager container on port 8090. The API Gateway is now visible in the API Gateway Manager topology view.

