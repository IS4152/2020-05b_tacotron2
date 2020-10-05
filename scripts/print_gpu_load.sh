#!/usr/bin/env bash

# SSHs into all GPU-enabled cluster machines and prints a summary of their nvidia-smi info, sorted in asc order.

XGPHOSTS="xgpa0 xgpa1 xgpa2 xgpa3 xgpa4 xgpb0 xgpb1 xgpb2 xgpc0 xgpc1 xgpc2 xgpc3 xgpc4 xgpc5 xgpc6 xgpc7 xgpc8 xgpc9 xgpd0 xgpd1 xgpd2 xgpd3 xgpd4 xgpd5 xgpd6 xgpd7 xgpd8 xgpd9 xgpe0 xgpe1 xgpe2 xgpe3 xgpe4 xgpe5 xgpe6 xgpe7 xgpe8 xgpe9 xgpe10 xgpe11 xgpf0 xgpf1 xgpf2 xgpf3 xgpf4 xgpf5 xgpf6 xgpf7 xgpf8 xgpf9 xgpf10 xgpf11 cgpa0 cgpa1 cgpa2 cgpa3 cgpb0"
# XGPHOSTS="xgpa0 cgpb0"

echo $XCNHOSTS $XGPHOSTS | tr ' ' '\n' | \
    parallel --timeout 5 \
    'ssh -oBatchMode=yes -oStrictHostKeyChecking=no -q {} '"'"'nvidia-smi --format=csv,noheader --query-gpu=index,name,memory.free,memory.used,memory.total,utilization.gpu | awk '\'\\\'\''{print "{}	 " $0}'\'\\\'\'' && echo "{}	" $(nvcc --version | grep release) && echo {}'\' 2> /dev/null | \
    sort
