#! /usr/bin/env bash

if ! command -v protoc &> /dev/null ; then
    brew install protobuf
fi

touch __init__.py

for proto in `ls *.proto`; do
    protoc --python_out=. $proto
done

for py in `ls messages_*.py`; do
    sed -i '' -e 's/import m/import TurtleRabbitSSL.proto2.m/g' $py
done