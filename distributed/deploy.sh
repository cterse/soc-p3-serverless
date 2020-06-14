#!/bin/sh

# perform the same action on all services, defaulting to deploy
COMMAND=${1:-deploy}

pushd components/emitter/
serverless $COMMAND
popd

cd logistics
serverless $COMMAND

pushd merchant
serverless $COMMAND &
popd

pushd labeler
serverless $COMMAND &
popd

pushd wrapper
serverless $COMMAND &
popd

pushd packer
serverless $COMMAND &
popd
