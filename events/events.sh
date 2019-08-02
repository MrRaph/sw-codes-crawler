#!/bin/bash

rm -f /tmp/events.html
python3 ./sw-events.py
aws s3 cp /tmp/events.html s3://sw-codes-tendancieu-eu-west-1/events.html --acl public-read --profile sw

#rm -f /tmp/events.html
killall -9 /usr/lib/chromium-browser/chromium-browser-v7
