from emissor.persistence.persistence import ScenarioStorage
from emissor.representation.scenario import TextSignal, Modality
from cltl.combot.event.emissor import TextSignalEvent
import json
import os


def create_textsignal(scenario_id, current_folder, annotation):

    storage = ScenarioStorage(current_folder)
    scenario = storage.load_scenario(scenario_id)
    text_signals = scenario.get_signals(Modality.TEXT)
    scenario._signals[Modality.TEXT] = []
    scenario.scenario.signals['text'] = './text_new.json'

    for turn in annotation:
        signal = TextSignal.for_scenario(scenario_id, turn['start'], turn['end'], None, turn['text'])
        TextSignalEvent.add_agent_annotation(signal, turn['speaker'])
        scenario.append_signal(signal)
        storage.save_scenario(scenario)


if __name__ == '__main__':
    directory = 'emissor_original'

    for participant_directory in os.listdir(directory):
        participant = os.path.join(directory, participant_directory)
        participant_json = os.path.join(participant, 'speakers_annotated.json')
        if os.path.exists(participant_json):
            with open(participant_json) as infile:
                participant_data = json.load(infile)

            participant_annotation = participant_data['annotation']
            scen_id = participant_data['emissor_scenario']
            create_textsignal(scen_id, participant, participant_annotation)

    # with open('emissor_original/en_09/speakers_annotated.json') as infile:
    #     ann = json.load(infile)
    #
    # create_textsignal('230503_132141_01c7ed0e-90d2-44a4-bd4d-85d59266cea7',
    #                   'emissor_original/en_09',
    #                   ann)
