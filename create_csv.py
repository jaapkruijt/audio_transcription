import pandas as pd
import json
import os

if __name__ == '__main__':
    directory = 'emissor_original'

    for participant in os.listdir(directory):
        participant_data = os.path.join(directory, participant, 'speakers_annotated.json')
        if os.path.exists(participant_data):
            with open(participant_data) as infile:
                annotated_file = json.load(infile)

            annotations = annotated_file['annotation']
            df = pd.DataFrame.from_dict(annotations)
            csv_out = os.path.join(directory, participant, 'speakers_annotated.csv')
            df.to_csv(csv_out)




