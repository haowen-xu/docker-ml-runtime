#!/bin/bash

set -e

# Deploy the timezone settings
[ "x${TZ}" != "x" ] && \
    [ -f "/usr/share/zoneinfo/$TZ" ] && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Execute the program
exec "$@"
