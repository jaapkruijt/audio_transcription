#!/bin/bash

#INPUT_FILES="audio_expeditienext/*"
#INPUT_FILES="audio_alleskids_day1/*"
INPUT_FILES="audio_alleskids_day2/*"
#INPUT_FILES="tests/*"
OUTPUT_DIR="./transcriptions"

source venv/bin/activate

for f in $INPUT_FILES
do
  echo "transcribing $f..."
  caffeinate whisper $f --model large --language Dutch --output_dir $OUTPUT_DIR
done

