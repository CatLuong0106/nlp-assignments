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
        self.dictionary = []
        self.results = []

    def read_dictionary(self):
        dictionary_path = self.data_path / Path(self.file_names[0])
        with open(dictionary_path, "r") as file:
            dict_lines = file.readlines()
            for line in dict_lines:
                self.dictionary.append(line.strip("\n").split(" "))
        print(self.dictionary)
        
    def dfs(self):
        pass

    def print_results(self):
        format = "WORD=<word> POS=<pos> ROOT=<root> SOURCE=<source> PATH=<path array>"
        pass


def main():
    parser = ArgumentParser()
    parser.add_argument("-p","--path", default="", required=True, help="Insert the path of the data folder")
    args = parser.parse_args()
    
    data_path = Path(args.path)
    
    morphology = Morphology(data_path=data_path)
    morphology.read_dictionary()


if __name__ == "__main__":
    main()
