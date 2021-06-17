#!/usr/bin/bash
echo "Running PDAP/DHIS2 Session Encrypter"
(cd webserver && node node_modules/ts-node/dist/bin.js index.ts)
