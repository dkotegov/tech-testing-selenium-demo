#!/usr/bin/env bash

java -jar selenium-server-standalone-2.48.2.jar \
    -role node \
    -hub http://localhost:4444/grid/register \
    -Dwebdriver.chrome.driver="./chromedriver" \
    -browser browserName=chrome,maxInstances=1 \
    -browser browserName=firefox,maxInstances=1
