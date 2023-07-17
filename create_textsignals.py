from emissor.persistence.persistence import ScenarioStorage
from emissor.representation.scenario import TextSignal


def create_textsignal(scenario_id, current_folder, annotation):

    storage = ScenarioStorage(current_folder)
    scenario = storage.load_scenario(scenario_id)

    for turn in annotation:
        signal = TextSignal.for_scenario(scenario_id, turn['start'], turn['end'], turn['text'])
        scenario.append_signal(signal)
        storage.save_scenario(scenario)