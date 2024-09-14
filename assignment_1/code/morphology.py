import re
import pprint
from argparse import ArgumentParser
from pathlib import Path
from collections import defaultdict


class Morphology:
    def __init__(self, dict_path, rule_path, test_path) -> None:
        self.dict_path = dict_path
        self.rule_path = rule_path
        self.test_path = test_path

        self.dictionary = []
        self.rules = []
        self.test = []
        self.results = set()
        self.printed_results = defaultdict(list)

        self.default_path = "-"
        self.default_pos = "noun"
        self.default_source = "default"

    def load_data(self) -> None:
        dictionary_path = Path(self.dict_path)
        rule_path = Path(self.rule_path)
        test_path = Path(self.test_path)

        with open(dictionary_path, "r") as file:
            dict_lines = file.readlines()
            for line in dict_lines:
                formatted_line = line.strip("\n").split(" ")
                if len(formatted_line) == 2:
                    root, pos = formatted_line
                    word = root
                else:
                    word, pos, _, root = formatted_line[0:4]

                self.dictionary.append({"word": word, "root": root, "pos": pos})

        with open(rule_path, "r") as file:
            pattern = r"(\d+)\s+(PREFIX|SUFFIX)\s+(\S+)\s+(\S+)\s+(\S+)\s+->\s+(\S+)"
            rule_lines = file.readlines()
            for line in rule_lines:
                matches = re.findall(pattern, line)
                list_matches = list(matches[0])
                match_val = {
                    "ID": list_matches[0],
                    "AFFIX_KEY": list_matches[1],
                    "AFFIX": list_matches[2],
                    "REP": list_matches[3],
                    "OLD_POS": list_matches[4],
                    "NEW_POS": list_matches[5],
                }
                self.rules.append(match_val)

        with open(test_path, "r") as file:
            test_lines = file.readlines()
            for line in test_lines:
                self.test.append(line.strip("\n").split(" ")[0])

        # Print for testing:

        # print("DICTIONARY: ")
        # pprint.pprint(self.dictionary)
        # print("\n")

        # print("RULES: ")
        # pprint.pprint(self.rules)
        # print("\n")

        # print("TEST DATA: ")
        # pprint.pprint(self.test)
        # print("\n")

    def get_results(self) -> None:

        # DFS to get all possible derivations from a word
        def dfs(word, path, source, pos):
            # Result to be appended
            result = {
                "word": word,
                "pos": pos,
                "source": source,
                "root": root,
                "path": path,
            }

            # If result is unique then added to the results list
            if result not in results:
                results.append(result)

            for rule in self.rules:
                # There must not be two similar 'ID's for the path
                # POS must match the 'OLD_POS'
                if rule["ID"] not in path and rule["OLD_POS"] == pos:
                    new_path = path + [rule["ID"]]
                    # Check to see if new path has been visited or not to avoid infinite loop
                    if tuple(new_path) not in visited:
                        # Add new path to the visited set
                        visited.add(tuple(new_path))

                        # PREFIX Logic
                        if rule["AFFIX_KEY"] == "PREFIX":
                            if rule["REP"] == "-":
                                # Prepend 'AFFIX' to word
                                new_word = rule["AFFIX"] + word
                                dfs(
                                    new_word,
                                    new_path,
                                    "morphology",
                                    rule["NEW_POS"],
                                )
                            elif word.startswith(rule["REP"]):
                                # Replace the prefix of length equal to 'REP' with 'AFFIX'
                                new_word = rule["AFFIX"] + word[len(rule["REP"]) :]
                                dfs(
                                    new_word,
                                    new_path,
                                    "morphology",
                                    rule["NEW_POS"],
                                )

                        # SUFFIX Logic
                        if rule["AFFIX_KEY"] == "SUFFIX":
                            if rule["REP"] == "-":
                                # Append 'AFFIX' to word
                                new_word = word + rule["AFFIX"]
                                dfs(
                                    new_word,
                                    new_path,
                                    "morphology",
                                    rule["NEW_POS"],
                                )
                            elif word.endswith(rule["REP"]):
                                # Replace the suffix of length equal to 'REP' with 'AFFIX'
                                new_word = word[: -len(rule["REP"])] + rule["AFFIX"]
                                dfs(
                                    new_word,
                                    new_path,
                                    "morphology",
                                    rule["NEW_POS"],
                                )

        # Get all possible derivations for each word in dictionary using DFS
        results = []
        for word in self.dictionary:
            visited = set()
            word_val, root, pos = word.values()
            dfs(word_val.lower(), [], "dictionary", pos)

        self.results = results

        # Print for testing:
        # pprint.pprint(results)
        # print(len(results))

    def print_results(self) -> None:
        # format = "WORD=<word> POS=<pos> ROOT=<root> SOURCE=<source> PATH=<path array>"
        for word in self.test:
            # Set of default components
            root = word
            pos = self.default_pos
            source = self.default_source
            path_str = self.default_path

            # Parameter to check if the word is found in the list of possible derivations
            used = False
            for result in self.results:
                if result["word"] == word:
                    path = result["path"]
                    if path:
                        path_str = path[0]
                        for i in range(1, len(path)):
                            path_str += f",{path[i]}"
                    else:
                        path_str = self.default_path

                    pos = result["pos"]
                    root = result["root"]
                    source = result["source"]
                    used = True
                    self.printed_results[word].append(
                        {
                            "WORD": word,
                            "POS": pos,
                            "ROOT": root,
                            "SOURCE": source,
                            "PATH": path_str,
                        }
                    )

            if not used:
                self.printed_results[word].append(
                    {
                        "WORD": word,
                        "POS": pos,
                        "ROOT": root,
                        "SOURCE": source,
                        "PATH": path_str,
                    }
                )

            # Sort printed results alphabetically by 'POS'
            self.printed_results[word].sort(key=lambda item: item["POS"])

        # Code for testing:

        # print(self.printed_results)
        # with open("yourTrace.txt", "w") as f:
        #     for word in self.printed_results:
        #         for line in self.printed_results[word]:
        #             f.write(
        #                 f"WORD={line['WORD']}\tPOS={line['POS']}\tROOT={line['ROOT']}\tSOURCE={line['SOURCE']}\tPATH={line['PATH']}\n"
        #             )
        #         f.write("\n")

        # NOTE: Print to screen for grading!
        for word in self.printed_results:
            for line in self.printed_results[word]:
                print(
                    f"WORD={line['WORD']}\tPOS={line['POS']}\tROOT={line['ROOT']}\tSOURCE={line['SOURCE']}\tPATH={line['PATH']}"
                )
            print("")


def __main__():
    # NOTE:
    # Run `python3 morphology.py Dict0.txt Rules0.txt Test0.txt`

    parser = ArgumentParser(description="Morphologial Analyzer")

    parser.add_argument("dict_file", type=str, help="Dictionary file")
    parser.add_argument("rules_file", type=str, help="Rules file")
    parser.add_argument("test_file", type=str, help="Test file")
    args = parser.parse_args()

    morphology = Morphology(
        dict_path=args.dict_file, rule_path=args.rules_file, test_path=args.test_file
    )
    morphology.load_data()
    morphology.get_results()
    morphology.print_results()


if __name__ == "__main__":
    __main__()
