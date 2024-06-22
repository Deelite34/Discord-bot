#!/bin/bash
set -e
# https://github.com/sudo-bmitch/docker-base/blob/f1b7e1a775d41d93b354037f193c2dcc8946ee34/bin/entrypointd.sh#L66
# Handle a kill signal before the final "exec" command runs
trap "{ exit 0; }" TERM INT

umask 0000

exec python bot.py