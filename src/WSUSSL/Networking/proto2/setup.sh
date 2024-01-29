#! /usr/bin/env bash

if ! command -v protoc &> /dev/null ; then
    if [[ "$OSTYPE" == "darwin" ]]; then
        brew install protobuf
    elif [[ "$OSTYPE" == "linux-gnu*" ]]; then
        apt install -y protobuf-compiler
    fi

fi

touch __init__.py
 
git clone https://github.com/RoboCup-SSL/grSim.git
cp grSim/src/proto/*.proto .

for proto in `ls *.proto`; do
    protoc --python_out=. $proto
done

rm -rf grSim *.proto