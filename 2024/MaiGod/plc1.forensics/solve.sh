#!/bin/bash

strings recurso/plc.pcap | \
    awk '/[0-9]:.+/' | \
    sort | cut -c 3- | \
    tr -d '\n' | \
    tee recurso/flag.txt

echo