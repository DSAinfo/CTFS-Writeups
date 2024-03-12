#!/bin/bash

cat -A recurso/flags.txt | \
    grep 'MAPNA{.*}\^M\$' | \
    rev | cut -c 4- | rev
