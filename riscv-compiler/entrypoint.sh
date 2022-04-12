#!/bin/bash

# This file is used in Docker
# Executed passed commands with passed uid/gid
echo "(UID:$USER_ID,GID:$GROUP_ID): $@"
usermod -u $USER_ID -o user
groupmod -g $GROUP_ID user

# You have to use gosu due to an issue regarding tty.
# "make serve" does not work if su is used.
#su user -c "$@"
exec /usr/sbin/gosu user "$@"

