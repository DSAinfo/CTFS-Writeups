#!/bin/bash

cat drawing.flag.svg | grep "</tspan" | cut -d ">" -f2 | cut -d "<" -f1 | tr -d "\n" | tr -d " "