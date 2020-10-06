#!/usr/bin/env bash

# Copies normalized EmoV-DB dataset from cgpb0 into the local machine's hard drive.
# You may want to check your machine doesn't already have the files:
# ls /temp/e-liang/out

mkdir -p /temp/e-liang
scp -r cgpb0:/temp/e-liang/out /temp/e-liang/out