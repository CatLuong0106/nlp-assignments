import math
from pathlib import Path
from argparse import ArgumentParser
from collections import Counter


class Ngrams:
    def __init__(
        self, train_file: str = "train1.txt", test_file: str = "test1.txt"
    ) -> None:
        self.unigram_vocab = {}
        self.unigram_test_lines = []
        self.bigram_vocab = []
        self.bigram_test_lines = []

        self.train_path = Path(train_file)
        self.test_path = Path(test_file)

        self.beginning_symbol = "<s>"
        self.beginning_symbol_freq = 0

        self.test_sentences = []
        self.unigram_results = []
        self.bigram_results = []
        self.bigram_smoothing_results = []

    def load_data(self):
        with open(self.train_path, "r") as f:
            lines = f.readlines()
            temp = []
            for line in lines:
                # Strip the new line symbol and empty string from the line
                temp_line = [l.lower() for l in line.strip("\n").split(" ") if l != ""]
                temp += temp_line
                self.bigram_vocab.append([self.beginning_symbol] + temp_line)
                self.beginning_symbol_freq += 1

            self.unigram_vocab = Counter(temp)

        with open(self.test_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                temp_line = [l.lower() for l in line.strip("\n").split(" ") if l != ""]
                self.test_sentences.append(line.strip("\n"))
                self.unigram_test_lines.append(temp_line)
                self.bigram_test_lines.append([self.beginning_symbol] + temp_line)

        # print(self.test_sentences)
        # print("Train Frequency: ", self.bigram_vocab)
        # print("Test Sentences: ", self.bigram_test_lines)

    def generate_bigrams_vocab(self):
        temp = []
        for sentence in self.bigram_vocab:
            for i in range(len(sentence) - 1):
                temp.append((sentence[i], sentence[i + 1]))
        self.bigram_vocab = Counter(temp)

    def predict(self) -> None:
        # Word Occurences Size
        N = sum(self.unigram_vocab.values())

        # Vocabulary Size
        V = len(self.unigram_vocab)

        # Unigram no smoothing
        def unigram(sentence: list) -> float:
            probability = 1
            for word in sentence:
                base_word = word.lower()
                if base_word in self.unigram_vocab:
                    probability *= self.unigram_vocab[base_word] / N
            return math.log(probability, 2)

        # Generate bigrams vocabulary
        self.generate_bigrams_vocab()

        # Bigrams no smoothing
        def bigram(sentence: list) -> float:
            probability = 1
            if len(sentence) < 2:
                return 0

            for i in range(len(sentence) - 1):
                unigram = sentence[i]
                bigram = (sentence[i], sentence[i + 1])
                if bigram in self.bigram_vocab:
                    if unigram == self.beginning_symbol:
                        probability *= (
                            self.bigram_vocab[bigram] / self.beginning_symbol_freq
                        )
                        continue
                    probability *= (
                        self.bigram_vocab[bigram] / self.unigram_vocab[unigram]
                    )
                else:
                    return 0

            return probability

        # Bigrams with Laplacian Add-one Smoothing
        def bigram_with_smoothing(sentence: list) -> float:
            probability = 1
            if len(sentence) < 2:
                return 0

            for i in range(len(sentence) - 1):
                unigram = sentence[i]
                bigram = (sentence[i], sentence[i + 1])
                if unigram == self.beginning_symbol:
                    probability *= (self.bigram_vocab[bigram] + 1) / (
                        self.beginning_symbol_freq + V
                    )
                    continue
                probability *= (self.bigram_vocab[bigram] + 1) / (
                    self.unigram_vocab[unigram] + V
                )

            return probability

        unigram_res = []
        for sentence in self.unigram_test_lines:
            val = unigram(sentence)
            unigram_res.append("{:.4f}".format(val))
        self.unigram_results = unigram_res

        bigram_res = []
        for sentence in self.bigram_test_lines:
            val = bigram(sentence)
            if not val:
                bigram_res.append("undefined")
            else:
                val = math.log(val, 2)
                bigram_res.append("{:.4f}".format(val))
        self.bigram_results = bigram_res

        bigram_with_smoothing_res = []
        for sentence in self.bigram_test_lines:
            val = bigram_with_smoothing(sentence)
            val = math.log(val, 2)
            bigram_with_smoothing_res.append("{:.4f}".format(val))
        self.bigram_smoothing_results = bigram_with_smoothing_res
        
        # Print for checking results
        # print("Unigram Results: ", self.unigram_results)
        # print("Bigram Results: ", self.bigram_results)
        # print("Bigrams smoothing results: ", self.bigram_smoothing_results)

    def print_results(self) -> None: 
        for idx, sent in enumerate(self.test_sentences): 
            print(f"S = {sent}")
            print(f"Unsmoothed Unigrams, logprob(S) = {self.unigram_results[idx]}")
            print(f"Unsmoothed Bigrams, logprob(S) = {self.bigram_results[idx]}")
            print(f"Smoothed Bigrams, logprob(S) = {self.bigram_smoothing_results[idx]}")
            if idx != len(self.test_sentences) - 1:
                print()

def __main__():
    parser = ArgumentParser(
        description="Get path training and test files for Ngrams model"
    )
    parser.add_argument("train_file", default="train1.txt")
    parser.add_argument("test_file", default="test1.txt")
    args = parser.parse_args()

    ngrams = Ngrams(args.train_file, args.test_file)
    ngrams.load_data()
    ngrams.predict()
    ngrams.print_results()


if __name__ == "__main__":
    __main__()
