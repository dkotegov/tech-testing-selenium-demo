#!/usr/bin/env bash

java -Dwebdriver.chrome.driver="./chromedriver" \
    -Dwebdriver.gecko.driver="./geckodriver" \
    -jar selenium-server-standalone-3.0.1.jar \
    -role node \
    -hub http://localhost:4444/grid/register \
    -browser browserName=chrome,maxInstances=2 \
    -browser browserName=firefox,maxInstances=2
