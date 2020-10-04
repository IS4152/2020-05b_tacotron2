#!/usr/bin/env python3

import glob
import math
import numpy as np
import os
import random
import re

files = sorted(glob.glob('../emovdb/*/*/*'))

dataLookup = {}
with open('cmuarctic.data', 'r') as f:
    dataLines = f.readlines()
    p = re.compile('^\( arctic_a0(\d{3}) "(.*)"')
    for line in dataLines:
        m = p.match(line)
        if m is not None:
            (num, phrase) = m.group(1, 2)
            dataLookup[num] = phrase
            if num == '066':
                dataLookup['666'] = phrase # To accomodate a typo in the file jenie/aud_am/amused_57-84_0666.wav

p = re.compile('.*_0(\d{3}).wav')
transformedFiles = [f"{os.path.abspath(file)}|{dataLookup[p.match(file).group(1)]}\n" for file in files if p.match(file) is not None]

random.shuffle(transformedFiles)
# print(transformedFiles)

splits = [(0.88, "train"), (0.10, "test"), (0.02, "val")]
splitLens = [math.floor(split * len(transformedFiles)) for (split, _) in splits]
cumulativeSplitLens = np.cumsum(splitLens)

for (i, (_, name)) in enumerate(splits):
    filesToExport = transformedFiles[slice(cumulativeSplitLens[i] - splitLens[i], cumulativeSplitLens[i])]
    with open(f'filelists/emovdb_audio_text_{name}_filelist.txt', 'w+') as f:
        f.writelines(filesToExport)