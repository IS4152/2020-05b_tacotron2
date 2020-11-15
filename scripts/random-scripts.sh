# Copypasta commands

# Get summary of variations in dataset
mediainfo */*/*.wav | grep -v name | grep -v Duration | grep -v Stream | grep -v 'File size' | sort | uniq

# Get list of all 44.1 kHz files
pcregrep -M '^Complete.+?\n.+?44\.1 kHz' samplingrates.txt | grep Complete | cut -d: -f2 | tr -d '

# Normalize files
ls */*/*.wav | xargs -I % sh -c 'mkdir -p ../out/$(dirname %) && sox % --rate 16000 -c 1 -b 32 ../out/%'
# Actually LJ Speech is 16 bit
ls */*/*.wav | xargs -I % sh -c 'mkdir -p ../out/$(dirname %) && sox % --rate 16000 -c 1 -b 16 ../out/%'

# Process MELD
ls *.mp4 | xargs -I % sh -c 'ffmpeg -i % -q:a 0 -map a $(basename -s mp4 %).aac'
ls *..aac | xargs -I % sh -c 'faad -d -o $(basename -s ..aac %).faad.wav %'
ls *.faad.wav | xargs -I % sh -c 'sox % --rate 16000 -c 1 -b 16 $(basename -s .faad.wav %).final.wav'