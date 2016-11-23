#!/usr/bin/env bash


tr -s ' ' '\n' < $1 | sort | uniq -c | sort -nr | tr -s ' ' ' '