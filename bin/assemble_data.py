__author__ = '@oscarmarinmiro @ @outliers_es'

import sys
import json
import pprint
import os
import glob
import re
import math

# Pass directory as argument!! (for concurrent analysis)

# Read config file

CONFIG_FILE = "../config/config.oscar.json"

FILE_OUT = "datamaster.json"

my_config = json.load(open(CONFIG_FILE, "rb"))

base_dir = my_config['dir_out']

my_data = []

for i, entry in enumerate(my_config['sources']):

    print "Parsing chapter %d *" % (i) + entry['title'] + "*"

    transcript_files_path = os.path.join(base_dir, str(i), 'transcript*.json')

    files = glob.glob(transcript_files_path)

    chapter_count = 0
    timings = []

    for file in files:

        m = re.search('transcript(\d+)\.json', file)

        if m:
            split_number = int(m.group(1))

            print " - segment %d - " % split_number

            time_offset_seconds = split_number * my_config['split_seconds']
            # pprint.pprint([split_number, time_offset_seconds])

            segment_data = json.load(open(file, "rb"))

            if 'results' in segment_data:
                for result in segment_data['results']:

                    for keyword in result['keywords_result'].keys():
                        chapter_count += len(result['keywords_result'][keyword])

                        for key_entry in result['keywords_result'][keyword]:

                            timings.append({'begin': key_entry['start_time'] + time_offset_seconds,
                                            'end': key_entry['end_time'] + time_offset_seconds,
                                            'length': key_entry['end_time'] - key_entry['start_time'],
                                            'link': entry['url'] + "&t=" + str(int(math.floor(key_entry['start_time']+ time_offset_seconds))) + "s"
                            })



    my_data.append({'source_number': str(i), 'url': entry['url'], 'title': entry['title'], 'date': entry['date'], 'count': chapter_count, 'timings': timings})

pprint.pprint(my_data)

json.dump(my_data, open(FILE_OUT, "wb"), indent=4)

