#!/usr/bin/env python3

# Generates filelists/FILENAMEPREFIXfilelist.txt files that contain paths to training audio
# files with their transcripts.
# 
# By default, this script must be run from within the scripts folder, i.e.:
#
# $ cd <repo root>/scripts
# $ ./genfilelist.py

import glob
import math
import os
import random
import re

import numpy as np

#####
# Params

FILENAMEPREFIX = 'i_am_a_screw_up_and_forgot_to_set_this' # DO NOT COMMIT THIS UNCOMMENTED
# FILENAMEPREFIX = 'emovdb'
# FILENAMEPREFIX = 'emovdbwithljs'
# FILENAMEPREFIX = 'emovdbwithoutamused'

INCLUDE_EMOVDB = True
INCLUDE_LJS = False

SHOULD_REMOVE_AMUSED = True

SPLITS = [(0.98, "train"), (0.02, "val")]

EMOVDB_FILES = sorted(glob.glob('/temp/e-liang/out/*/*/*'))
EMOVDB_CMUARCTIC_PATH = '../cmuarctic.data' # Transcripts for emovdb dataset located in repo root
LJS_FOLDER = '/temp/e-liang/LJSpeech-1.1'
OUT_FOLDER = '../filelists/' # Folder located in repo root

#####

def get_emovdb_lines():
    dataLookup = {}
    with open(EMOVDB_CMUARCTIC_PATH, 'r') as f:
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
    all_emovdb_lines = [f"{os.path.abspath(file)}|{dataLookup[p.match(file).group(1)]}\n" for file in EMOVDB_FILES if p.match(file) is not None]

    if SHOULD_REMOVE_AMUSED:
        all_emovdb_lines = [line for line in all_emovdb_lines if '/amused/' not in line and '/aud_am/' not in line]

    return all_emovdb_lines

def get_ljs_lines():
    metadata_lines = None
    with open(os.path.join(LJS_FOLDER, 'metadata.csv'), 'r') as f:
        metadata_lines = f.readlines()

    def metadata_line_to_dataset_line(line):
        [lj_id, _, normalized_transcript] = line.split('|') # From LJS README, each line contains ID, Transcription, Normalized Transcript
        filepath = os.path.join(LJS_FOLDER, f"{lj_id}.wav")
        return f"{filepath}|{normalized_transcript}"
    return list(map(metadata_line_to_dataset_line, metadata_lines))

dataset_lines = []
if INCLUDE_EMOVDB:
    dataset_lines = get_emovdb_lines() + dataset_lines
if INCLUDE_LJS:
    dataset_lines = get_ljs_lines() + dataset_lines
random.shuffle(dataset_lines)

splitLens = [math.floor(split * len(dataset_lines)) for (split, _) in SPLITS]
cumulativeSplitLens = np.cumsum(splitLens)

for (i, (_, name)) in enumerate(SPLITS):
    filesToExport = dataset_lines[slice(cumulativeSplitLens[i] - splitLens[i], cumulativeSplitLens[i])]
    filename = f"{FILENAMEPREFIX}_audio_text_{name}_filelist.txt"
    with open(os.path.join(OUT_FOLDER, filename), 'w+') as f:
        f.writelines(filesToExport)
