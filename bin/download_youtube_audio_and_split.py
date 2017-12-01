__author__ = '@oscarmarinmiro @ @outliers_es'

import json
import os
import glob

# Read config file

CONFIG_FILE = "../config/config.oscar.json"

my_config = json.load(open(CONFIG_FILE, "rb"))

# Create directories, download video audio in .wav format and split with ffmpeg

for i,entry in enumerate(my_config['sources']):

    home_dir = os.path.join(my_config['dir_out'], str(i))

    os.system("mkdir -p %s" % (home_dir))

    os.system("cd %s; youtube-dl '%s' --extract-audio   --audio-format wav   --audio-quality 16K" % (home_dir, entry['url']))

    # Get output wav and slice into 'split_seconds' units

    pattern = os.path.join(home_dir, "*.wav")

    wavs = glob.glob(pattern)

    if len(wavs) > 0:

        os.system("cd %s; ffmpeg -i '%s' -f segment -segment_time %d -c copy " % (home_dir, wavs[0], my_config['split_seconds']) + "out%03d.wav")

