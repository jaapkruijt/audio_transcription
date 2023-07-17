import json
import pandas as pd
from thefuzz import fuzz
import numpy as np
import re
import os

scenario_id = '230503_132141_01c7ed0e-90d2-44a4-bd4d-85d59266cea7'

part_2_start = {'en_09': 858.0, 'en_12': 828.0, 'en_13': 663.0, 'en_14': 739.0, 'en_17': 846.0, 'en_21': 685.0,
                'en_24': 646.0, 'ak_02': 530.0, 'ak_04': 594.0, 'ak_05': 679.0, 'ak_06': 0, 'ak_07': 930.0}


def get_robot_utterances(original_emissor):
    utterances = []
    for utterance in original_emissor:
        utterance_info = {'utt': {'whole': utterance['text'], 'parts': re.split(r"[.?!]", utterance['text'])}, 'begin': utterance['time']['start']}
        try:
            utterance_info['utt']['parts'].remove('')
        except ValueError:
            pass
        utterances.append(utterance_info)

    return utterances


def clean_and_combine_transcriptions(transcription_part1, transcription_part2, start_time=0.0):
    combined_transcription = []
    for segment in transcription_part1['segments']:
        segment.pop('id')
        segment.pop('seek')
        segment.pop('tokens')
        segment.pop('temperature')
        segment.pop('avg_logprob')
        segment.pop('compression_ratio')
        segment.pop('no_speech_prob')
        # delete duplicates?
        combined_transcription.append(segment)
    if transcription_part2:
        for segment in transcription_part2['segments']:
            segment.pop('id')
            segment.pop('seek')
            segment.pop('tokens')
            segment.pop('temperature')
            segment.pop('avg_logprob')
            segment.pop('compression_ratio')
            segment.pop('no_speech_prob')
            segment['start'] += start_time
            segment['end'] += start_time
            combined_transcription.append(segment)

    return combined_transcription


def match_and_remove(transcription_segment, utterance_parts):
    transcription_segment['speaker'] = 'robot'
    segments_split = transcription_segment['text'].split('.')
    try:
        segments_split.remove('')
    except ValueError:
        pass
    # for i in range(len(segments_split)):
    #     utterance_parts.pop(0)
    matched = len(segments_split)
    return matched


def find_match_by_timestamp(utterance, transcription_segment):
    robot_part_utterance = []
    segment_length = transcription_segment['end'] - transcription_segment['start']
    if transcription_segment['start'] - 4.0 <= utterance['begin'] <= transcription_segment['start'] + segment_length+2.0:
        match = fuzz.partial_ratio(transcription_segment['text'], utterance['utt']['parts'][0])
        if match > 80:
            matched = match_and_remove(transcription_segment, utterance['utt']['parts'])
            if len(utterance['utt']['parts']) > matched:
                robot_part_utterance = utterance['utt']['parts'][matched:]
    return robot_part_utterance


def annotate_speakers(transcription, robot_utterances, participant_no):
    robot_part_utterance = []
    for segment in transcription:
        if robot_part_utterance:
            match = fuzz.partial_ratio(segment['text'], robot_part_utterance[0])
            if match > 65:
                matched = match_and_remove(segment, robot_part_utterance)
                try:
                    for i in range(matched):
                        robot_part_utterance.pop(0)
                except IndexError:
                    print(f"Error: {segment['text']} at time {segment['start']} for participant {participant_no}")
            else:
                for utterance in robot_utterances:
                    robot_part_utterance = find_match_by_timestamp(utterance, segment)
                    if robot_part_utterance:
                        break
        else:
            for utterance in robot_utterances:
                robot_part_utterance = find_match_by_timestamp(utterance, segment)
                if robot_part_utterance:
                    break

    for segment in transcription:
        if 'speaker' not in segment:
            segment['speaker'] = 'human'

    return transcription


def annotate_files(directory):
    speakers_annotated = []
    for participant_no in os.listdir(directory):
        files = {'robot_utterances': {}, 'part1': {}, 'part2': {}}
        data = os.path.join(directory, participant_no)
        for datafile in os.listdir(data):
            if datafile.startswith('23'):
                emissor_path = os.path.join(data, datafile, 'text_processed.json')
                files['scenario_id'] = datafile
                with open(emissor_path) as emissor_file:
                    emissor = json.load(emissor_file)
                files['robot_utterances'] = get_robot_utterances(emissor)
            elif datafile == 'transcription':
                transcription_path = os.path.join(data, datafile)
                if not os.listdir(transcription_path):
                    continue
                else:
                    for part in os.listdir(transcription_path):
                        if part.endswith('part1.json'):
                            part_file = os.path.join(data, datafile, part)
                            with open(part_file) as infile:
                                part_dict = json.load(infile)
                            files['part1'] = part_dict
                        elif part.endswith('part2.json'):
                            part_file = os.path.join(data, datafile, part)
                            with open(part_file) as infile:
                                part_dict = json.load(infile)
                            files['part2'] = part_dict
        if not files['part1']:
            continue
        files['combined_parts'] = clean_and_combine_transcriptions(files['part1'], files['part2'],
                                                                   part_2_start[participant_no])
        annotated = annotate_speakers(files['combined_parts'], files['robot_utterances'], participant_no)
        annotated_with_metadata = {'participant': participant_no, 'emissor_scenario': files['scenario_id'],
                                   'annotation': annotated}
        annotated_file = json.dumps(annotated_with_metadata)
        with open(f'{data}/speakers_annotated.json', 'w') as outfile:
            outfile.write(annotated_file)




if __name__ == "__main__":
    annotate_files('emissor_original')


















