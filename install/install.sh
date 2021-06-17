#!/usr/bin/bash

installNode () {
    curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
    yum install -y nodejs
}

installPython(){
    pip3 install --upgrade pip
    pip3 install boto3
    pip3 install setuptools_rust
    pip3 install cryprography
}

installDeps(){
    (cd webserver && npm i)
}

installNode
installDeps



