#!/usr/bin/env bash

tr '[A-Z]' '[a-z]' < $1 |tr  tr -sc '[A-Z][a-z]' '[\012*]' | sort | uniq -c | sort -nr
