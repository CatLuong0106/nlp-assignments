import os
import argparse
from argparse import ArgumentParser
from pathlib import Path


class Morphology:
    def __init__(self, data_path):
        self.data_path = data_path
        self.file_names = ["Dict0.txt", "Rules0.txt", "Test0.txt", "Trace0.txt"]
        self.rules = [
            ["SUFFIX", "s", "-", "noun", "noun"],
            ["SUFFIX", "s", "-", "verb", "verb"],
            ["SUFFIX", "iest", "y", "adjective", "adjective"],
            ["SUFFIX", "y", "-", "noun", "adjective"],
            ["SUFFIX", "er", "-", "verb", "noun"],
            ["PREFIX", "un", "-", "adjective", "adjective"],
            ["PREFIX", "anti", "-", "noun", "adjective"],
        ]
        self.source = ["default", "dictionary", "morphology"]
        self.dictionary = []
        self.test = []
        self.results = set()
        self.default_path = "-"

    def load_data(self):
        dictionary_path = self.data_path / Path(self.file_names[0])
        test_path = self.data_path / Path(self.file_names[2])

        print("LOADING DATA: \n")
        with open(dictionary_path, "r") as file:
            dict_lines = file.readlines()
            for line in dict_lines:
                self.dictionary.append(line.strip("\n").split(" "))
        print("Dictionary loaded: ", self.dictionary)
        print("\n")

        with open(test_path, "r") as file:
            test_lines = file.readlines()
            for line in test_lines:
                self.test.append(line.strip("\n").split(" ")[0])
        print("Test data loaded: ", self.test)

    def dfs(self):
        for word in self.test:
            for entry in self.dictionary:
                if word == entry[0]:
                    if len(entry) < 4:
                        self.results.add(
                            f"WORD={entry[0]} POS={entry[1]} ROOT={entry[0]} SOURCE={self.source[1]} PATH={self.default_path}"
                        )
                    else:
                        self.results.add(
                            f"WORD={entry[0]} POS={entry[1]} ROOT={entry[3]} SOURCE={self.source[1]} PATH={self.default_path}"
                        )
            # TODO: Implement exhaustive DFS logic for morphology

    def print_results(self):
        format = "WORD=<word> POS=<pos> ROOT=<root> SOURCE=<source> PATH=<path array>"
        for result in self.results:
            print(result)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        default="",
        required=True,
        help="Insert the path of the data folder",
    )
    args = parser.parse_args()

    data_path = Path(args.path)

    morphology = Morphology(data_path=data_path)
    morphology.load_data()
    morphology.dfs()
    morphology.print_results()


if __name__ == "__main__":
    main()
