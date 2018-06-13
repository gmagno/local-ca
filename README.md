# How to setup a local Certificate Authority for development purposes

Steps to make a local certificate authority and generate certificates for dev servers. Inspired by [this article](https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/ "How to Create Your Own SSL Certificate Authority for Local HTTPS Development").

1. Generate the root private key
```
$ openssl genrsa -des3 -out rootCA.key 2048
```

2. Generate the root certificate using the private key

```
$ openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1825 -out rootCA.pem
```

3. Convert the root certificate from .pem to .crt

```
$ openssl x509 -outform der -in rootCA.pem -out rootCA.crt
```

4. Add the root certificate to ubuntu local config directory

```
$ sudo cp rootCA.crt /usr/local/share/ca-certificates/
$ sudo update-ca-certificates
```

5. Create CA-Signed certificates for my dev servers by creating a private key and a CSR (certificate request)

```
$ mkdir -p dev-server && cp dev-server.py dev-server && cd dev-server
$ openssl genrsa -out dev-server.local.key 2048
$ openssl req -new -key dev-server.local.key -out dev-server.local.csr
$ openssl x509 -req -in dev-server.local.csr -CA ../rootCA.pem -CAkey ../rootCA.key \
-CAcreateserial -out dev-server.local.crt -days 1825 -sha256 \
-extfile ../dev-server.local.cfg
$ openssl x509 -outform PEM -in dev-server.local.crt -out dev-server.local.pem  # convert .crt to .pem
```

6. Copy the dev-server certificate and key to the server and run the test python script

```
$ cd .. && scp -r dev-server/ <user>@dev-server.local:~/
```
finally ssh into the dev-server.local and run the python script.

An https request on https://dev-server.local:4443 should open a secure connection with the server.

Do not forget to import the CA root certificate to the browser!
