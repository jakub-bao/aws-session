#!/usr/bin/bash

installNode () {
    curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
    yum install -y nodejs
}

installDeps(){
    (cd sessionIdEncrypter && npm i)
}

installNode
installDeps



