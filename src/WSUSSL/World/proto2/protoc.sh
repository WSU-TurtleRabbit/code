#! /usr/bin/env bash

if ! command -v protoc &> /dev/null ; then
    brew install protobuf
fi

touch __init__.py

for proto in `ls *.proto`; do
    protoc --python_out=. $proto
done

for py in `ls *.py`; do 
    mv $py $py.old
    cat $py.old | sed 's/import ssl/import WSUSSL.World.proto2.ssl/g' > $py
    rm $py.old
done

for py in `ls *.py`; do 
    mv $py $py.old
    cat $py.old | sed 's/import gr/import WSUSSL.World.proto2.gr/g' > $py
    rm $py.old
done

   