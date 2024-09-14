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
        def dfs(word, path, source, pos):
            for rule in self.rules:
                if rule["ID"] not in path:
                    if rule["OLD_POS"] == pos:
                        if tuple(path + [rule["ID"]]) not in visited:
                            visited.add(tuple(path))
                        else:
                            break

                        if rule["AFFIX_KEY"] == "PREFIX":
                            if rule["REP"] == "-":
                                dfs(
                                    rule["AFFIX"] + word,
                                    path + [rule["ID"]],
                                    "morphology",
                                    rule["NEW_POS"],
                                )
                            elif word.startswith(rule[3]):
                                dfs(
                                    word[len(rule["AFFIX"]) :] + rule[2],
                                    path + [rule["ID"]],
                                    "morphology",
                                    rule["NEW_POS"],
                                )

                        if rule["AFFIX_KEY"] == "SUFFIX":
                            if rule["REP"] == "-":
                                dfs(
                                    word + rule["AFFIX"],
                                    path + [rule["ID"]],
                                    "morphology",
                                    rule["NEW_POS"],
                                )
                            elif word.endswith(rule["REP"]):
                                dfs(
                                    word[: -len(rule["REP"])] + rule["AFFIX"],
                                    path + [rule["ID"]],
                                    "morphology",
                                    rule["NEW_POS"],
                                )

                        result = {
                            "word": word,
                            "pos": pos,
                            "source": source,
                            "root": root,
                            "path": path,
                        }
                        if result not in results:
                            results.append(result)

        results = []
        for word in self.dictionary:
            visited = set()
            word_val, root, pos = word.values()
            dfs(word_val.lower(), [], "dictionary", pos)

        # Print for testing:

        # pprint.pprint(results)
        # print(len(results))

        self.results = results

    def print_results(self):
        # format = "WORD=<word> POS=<pos> ROOT=<root> SOURCE=<source> PATH=<path array>"
        for word in self.test:
            pos = self.default_pos
            root = word
            source = self.default_source
            path_str = self.default_path
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

        for word in self.printed_results:
            for line in self.printed_results[word]:
                print(
                    f"WORD={line['WORD']}\tPOS={line['POS']}\tROOT={line['ROOT']}\tSOURCE={line['SOURCE']}\tPATH={line['PATH']}"
                )
            print("")


def __main__():
    # Example: python3 morphology.py Dict0.txt Rules0.txt Test0.txt

    parser = ArgumentParser(description="Morphologial Analyzer")
    # parser.add_argument(
    #     "-p",
    #     "--path",
    #     default="",
    #     required=True,
    #     help="Insert the path of the data folder",
    # )

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
