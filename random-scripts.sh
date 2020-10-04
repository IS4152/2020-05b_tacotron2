# Get summary of variations in dataset
mediainfo */*/*.wav | grep -v name | grep -v Duration | grep -v Stream | grep -v 'File size' | sort | uniq

# Get list of all 44.1 kHz files
pcregrep -M '^Complete.+?\n.+?44\.1 kHz' samplingrates.txt | grep Complete | cut -d: -f2 | tr -d '

# Normalize files
ls */*/*.wav | xargs -I % sh -c 'mkdir -p ../out/$(dirname %) && sox % --rate 16000 -c 1 -b 32 ../out/%'
