#!/bin/bash

# SPECCPU2017_DIR and CONFIG_FILE must be set externaly

cd ${SPECCPU2017_DIR}
source shrc
runcpu --config ${CONFIG_FILE} --action runsetup --define bits=64 --size test --tune=base 

