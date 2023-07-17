import json
import os


def preprocess_emissor(file_path):
    file = os.path.join(file_path, 'text.json')
    with open(file) as original_emissor:
        text = json.load(original_emissor)

    start_unix_time = text[1]['time']['start']

    for utterance in text:
        utterance['time']['start'] = (utterance['time']['start'] - start_unix_time)/1000
        utterance['text'] = utterance['text'].strip('\n')
        utterance['text'] = utterance['text'].strip()

    emissor_preprocessed = json.dumps(text)
    with open(f'{file_path}/text_processed.json', 'w') as outfile:
        outfile.write(emissor_preprocessed)


if __name__ == "__main__":
    directory = "emissor_original"

    for dir_name in os.listdir(directory):
        participant_data = os.path.join(directory, dir_name)
        for emissor_directory in os.listdir(participant_data):
            emissor = os.path.join(participant_data, emissor_directory)
            preprocess_emissor(emissor)
