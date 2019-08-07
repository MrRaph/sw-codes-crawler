#!/bin/bash

cd /opt/sw-codes-crawler/events/
rm -f /tmp/events.html

source env.vars

python3 ./sw-events.py
aws s3 cp /tmp/events.html s3://${bucket}/events.html --acl public-read --profile sw

rm -f /tmp/events.html /tmp/history_events__23456765432.txt
killall -9 /usr/lib/chromium-browser/chromium-browser-v7
