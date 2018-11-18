#!/bin/bash

# From https://github.com/jas-on/pre-commit-hadolint/blob/master/run_hadolint.sh


if which hadolint &> /dev/null $? != 0 ; then
    echo "Hadolint must be installed"
    exit 1
fi

hadolint "$@"
exit $?
