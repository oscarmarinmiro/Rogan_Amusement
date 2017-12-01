__author__ = '@oscarmarinmiro @ @outliers_es'

import sys
import json
import os
import glob
import re

# Pass directory as argument!! (for concurrent analysis)

# Read config file

CONFIG_FILE = "../config/config.oscar.json"

my_config = json.load(open(CONFIG_FILE, "rb"))

if len(sys.argv) == 2:
    my_home_dir = os.path.join(my_config['dir_out'], sys.argv[1])
    print my_home_dir

    audios = glob.glob(os.path.join(my_home_dir, "out*.wav"))

    # join keyworks by url-codified ",", surrounded by '"' url-coded: %22

    keyword_join = "%22" + "%2C".join(my_config['keywords']) + "%22"

    if len(audios) > 0:

        for audio in audios:

            # Get sequence from name

            m = re.match(r'.*out(\d+)\.wav$', audio)

            if m:
                sequence = m.groups()[0]

                # Build curl complete command and run

                destination_url = "%s?profanity_filter=false&keywords=%s&keywords_threshold=%f&max_alternatives=0" % (my_config['api_url'], keyword_join, my_config['keyword_threshold'])

                command = "curl -X POST -u %s:%s -o transcript%s.json --header 'Content-Type: audio/wav' --header 'Transfer-Encoding: chunked' --data-binary '@%s' '%s'" % (my_config['api_user'], my_config['api_password'], sequence, audio, destination_url)

                print "----"

                print command

                os.system("cd %s; %s" % (my_home_dir, command))

                print "===="


else:
    print "Only one argument is required: The directory number --> python ./recognize_dir.py directory_number"
