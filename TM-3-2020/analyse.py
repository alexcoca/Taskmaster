from collections import defaultdict
from typing import List, Dict, Optional, Set

import glob
import itertools
import json


def count_scenarios(file: str) -> Dict[str, int]:
    """

    Parameters
    ----------
    file
        Path to .json containing dialogues.

    Returns
    -------
    counts
        A mapping between scenarios and the number of times they occur
    """

    with open(file, 'r') as f:
        dialogues = json.load(f)  # type: List[dict]

    counts = defaultdict(int)

    for dialogue in dialogues:
        counts[dialogue['scenario']] += 1

    return counts


def get_scenarios(all_files: List[str]) -> Set[str]:
    """
    Returns a list of unique scenarios workers have used to produce dialogues.
    """

    scenarios = set()
    for file in all_files:
        with open(file, 'r') as f:
            dialogues_batch = json.load(f)

        for dialogue in dialogues_batch:
            scenarios.add(dialogue['scenario'])

    return scenarios


def aggregate(count_dicts: List[defaultdict]) -> Dict[str, int]:
    """
    Aggregates a list of default dictionaries by adding their counts for common keys.
    """

    # values default to 0
    aggregated = count_dicts[0]

    for key, val in itertools.chain(*[el.items() for el in count_dicts[1:]]):
        aggregated[key] += val

    return aggregated


def get_scenarios_stats(all_files: List[str]):
    """
    Counts unique scenarios in corpus.
    """
    per_file_counts = [count_scenarios(file) for file in all_files]
    return aggregate(per_file_counts)


def print_scenarios_info(all_files: List[str]):
    """
    Prints information about scenarios in the corpus.
    """

    sc_counts = get_scenarios_stats(all_files)
    print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in sc_counts.items()) + "}")
    print("")
    print(f"Number of scenarios: {len(sc_counts)}")
    print(f"Number of auto scenarios: {len([key for key in sc_counts.keys() if 'Auto' in key])}")


def print_scenario_instructions():
    pass


def get_scenarios_instructions(all_dialogues: List[str], idx: int = 0):
    """

    Parameters
    ----------
    idx
        Index of the file used to extract instructions. All files should
        be identical but this is an extra check.
    """

    # NB: checked all scenarios appear in all files
    file = all_dialogues[idx]
    with open(file, 'r') as f:
        dialogues = json.load(f)
    instructions = defaultdict(list)
    for dialogue in dialogues:
        # checked they are identical
        if dialogue['scenario'] in instructions and dialogue['scenario']:
            continue
        else:
            instructions[dialogue['scenario']] = dialogue['instructions']

    return instructions


def get_scenario_dialogues(all_dialogues: List[str], only_scenarios: Optional[Set[str]] = None) -> Dict[str, List[dict]]:
    """
    With default settings, returns all dialogues grouped by scenarios.

    Parameters
    ----------
    all_dialogues:
        List of .json files with dialogues
    only_scenarios
        Only return dialogues for scenarios specified in this set if specify.

    Returns
    -------
    A mapping from scenario name to a list of all dialogues for that scenario.
    """

    output = defaultdict(list)
    for file in all_dialogues:
        with open(file, 'r') as f:
            this_file_dialogues = json.load(f)
        for dialogue in this_file_dialogues:
            scenario = dialogue['scenario']
            if only_scenarios:
                if scenario in only_scenarios:
                    output[scenario].append(dialogue['utterances'])
            else:
                output[scenario].append(dialogue['utterances'])

    return output


if __name__ == '__main__':
    all_dialogues = glob.glob("data/*.json")
    # print_scenarios_info(all_dialogues)
    # save an example of each scenario
    # get_scenarios_instructions(all_dialogues)
    all_scenarios = get_scenarios(all_dialogues)
    scenario = 'Theaters temporarily closed'
    dialogues = get_scenario_dialogues(all_dialogues, only_scenarios={scenario})
    instructions = get_scenarios_instructions(all_dialogues)
    print("")