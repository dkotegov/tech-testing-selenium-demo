#!/usr/bin/env bash

java -Dwebdriver.chrome.driver="./chromedriver" \
    -Dwebdriver.gecko.driver="./geckodriver" \
    -jar selenium-server-standalone-3.11.0.jar \
    -role node \
    -hub http://127.0.0.1:4444/grid/register \
    -browser browserName=chrome,maxInstances=2 \
    -browser browserName=firefox,maxInstances=2
