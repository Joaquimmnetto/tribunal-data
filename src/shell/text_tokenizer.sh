#!/usr/bin/env bash

tokens='a-z0-9\n'

tr A-Z a-z < $1 | tr -sc 'a-z0-9\n' ' '