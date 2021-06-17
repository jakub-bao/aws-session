# PDAP / PEPFAR Session Provider

This is a service which provides PDAP session id to PEPFAR users.

## Installation
### Dependencies
Execute the installation script:
```console
./install/install.sh
```
The script will:

- Upgrade `pip3` python package manager
- Install `python` dependencies:
  - boto3
  - setuptools_rust
  - cryptography
- Install `node.js` @ `v14`
- Install `node.js` dependencies via `npm`

### nginx configuration
The session provider is a web-service providing an endpoint.  
Therefore, `nginx` has to be configured to allow outside access to the endpoint:
```nginx
# /etc/nginx/nginx.conf
http{
    server {
        location /pdapsession {
            proxy_pass http://localhost:3000/pdapsession;
        }
    }
}
```
Restart `nginx` to reflect the changes above
```console
sudo service nginx restart
```
No errors should appear.

### AWS credentials
The service must be able to retrieve `encryption key` from DATIM's AWS `secretmanager`.  
Reach to `PEPFAR/Systems` to authorize your DATIM instance and to receive `AWS Resource Name` & `AWS Region`
The two must be provided to the Session Provider via environment variables:
```console
export SECRET_ARN=abc
export SECRET_REGION=xyz
```

## Usage
Start the session provider by executing
```console
./startSessionProvider.sh
```
That should result in the following output
```console
# output:
> Running PDAP/DHIS2 Session Encrypter
> Session encrypter listening on http://localhost:3000/pdapsession
```

You can test the service is running properly by:

1. Logging into your `DATIM` instance, e.g.: `https://xyz.datim.org`
2. Navigating to: `https://xyz.pepfar.org/pdapsession`
3. The server output should be a single encrypted string, e.g.: `gAAAAABgy6U1_8XwqyMZripuy3V-6w-...`

The provided string will be used as a session ID for further communication between client and PDAP servers.  
The encrypted information inside is in fact a DHIS2 session id.

# How does it work?
The service consists of three microservices:

### Webserver
Standard `express/node.js` based webserver which listens @ `http://localhost/pdapsession`
It is responsible for the following:
1. Listening for API requests
2. Extracting `DHIS2 session ID` from the client's request   
2. Reaching to `Encryption key provider`
3. Requesting `DHIS2 Session ID` encryption from `Encrypter` service
4. Responding back to the pending API request

### Encryption key provider
`python` based microservice which retrieves an `encryption key` from `DATIM/secretmanager` service.

### Encrypter
`python` based microservice which can encrypt any `string` message using provided `encryption key`

