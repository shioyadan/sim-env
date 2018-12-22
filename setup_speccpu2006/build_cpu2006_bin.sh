#!/bin/bash

# SPECCPU2006_DIR and CONFIG_FILE must be set externaly

cd ${SPECCPU2006_DIR}
source shrc
runspec --config ${CONFIG_FILE} --action runsetup --size test --tune=base int fp

