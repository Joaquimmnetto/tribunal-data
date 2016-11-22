#!/usr/bin/env bash

tr 'A-Z' 'a-z' < $1 | tr -sc 'a-z:)(=' '\n' | sort | uniq -c | sort -nr
