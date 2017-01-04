#!/usr/bin/env bash

tokens='a-z0-9\n'
unicode=${2}

#TODO: manter ou ao menos normalizar acentos!
tr A-Z a-z < $1 | tr -sc ${tokens} ' '


