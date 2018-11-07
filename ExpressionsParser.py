def get_input():
    input_ = input().split()
    exp = list(input_[0])
    letter = input_[1]
    freq = int(input_[2])
    return exp, letter, freq


def find_shortest_word(exp, letter, freq):
    stack = []
    #INF = float("inf")
    INF = 1000000
    class language(object):
        def __init__(self, symbol=None):
            if symbol is None:
                # the min length of the word with letter^i
                # on prefix (suffix)
                self.prefix_lengths = [INF] * (freq + 5)
                self.suffix_lengths = [INF] * (freq + 5)
                # the min length of the word
                self.min_word = INF
                # the min length of the word containing letter^freq
                self.min_length = INF
                # the lengths of word consisting of only letters
                self.complete_lengths = []
            else:
                self.prefix_lengths = [INF] * (freq + 5)
                self.suffix_lengths = [INF] * (freq + 5)
                self.min_word = INF
                self.min_length = INF
                self.complete_lengths = []

                if symbol == letter:
                    self.min_word = 1
                    if freq == 1:
                        self.min_length = 1
                    else:
                        self.min_length = INF
                    self.complete_lengths.append(1)
                    self.prefix_lengths[1] = 1
                    self.suffix_lengths[1] = 1
                elif symbol == '1':
                    self.min_word = 0
                    self.complete_lengths.append(0)
                else:
                    self.min_word = 1
                    self.min_length = INF

    def make_step(symb):
        if symb == '+':
            if (len(stack) < 2):
                raise AttributeError("regular expression is incorrect")
            b, a = stack.pop(), stack.pop()
            stack.append(unite(a, b))
        elif symb == '.':
            if (len(stack) < 2):
                raise AttributeError("regular expression is incorrect")
            b, a = stack.pop(), stack.pop()
            stack.append(concat(a, b))
        elif symb == '*':
            if (len(stack) < 1):
                raise AttributeError("regular expression is incorrect")
            a = stack.pop()
            stack.append(closure(a))
        else:
            stack.append(language(symb))


    def unite(a, b):
        c = language()
        c.min_word = min(a.min_word, b.min_word)
        c.min_length = min(a.min_length, b.min_length)
        c.complete_lengths = list(set(a.complete_lengths + b.complete_lengths))
        c.prefix_lengths = [min(i, j) for i, j in zip(a.prefix_lengths, b.prefix_lengths)]
        c.suffix_lengths = [min(i, j) for i, j in zip(a.suffix_lengths, b.suffix_lengths)]
        return c

    def concat(a, b):
        c = language()
        c.min_word = a.min_word + b.min_word
        c.complete_lengths = []
        for i in a.complete_lengths:
            for j in b.complete_lengths:
                if (i + j) < freq + 5:
                    c.complete_lengths.append(i + j)

        c.prefix_lengths = [min(i + b.min_word, INF) for i in a.prefix_lengths]
        for i in a.complete_lengths:
            for j in range(len(b.prefix_lengths)):
                if (i + j) < (freq + 5):
                    c.prefix_lengths[i + j] = min(c.prefix_lengths[i + j], i + b.prefix_lengths[j], INF)

        c.suffix_lengths = [min(a.min_word + i, INF) for i in b.suffix_lengths]
        for i in b.complete_lengths:
            for j in range(len(a.suffix_lengths)):
                if (i + j) < (freq + 5):
                    c.suffix_lengths[i + j] = min(c.suffix_lengths[i + j], i + a.suffix_lengths[j], INF)

        c.min_length = min(a.min_length + b.min_word, a.min_word + b.min_length, INF)
        for i in range(len(a.suffix_lengths)):
            for j in range(len(b.prefix_lengths)):
                if (i + j) >= freq:
                    c.min_length = min(c.min_length, a.suffix_lengths[i] + b.prefix_lengths[j])

        return c


    def closure(a):
        c = language()
        c.min_word = 0
        c.complete_lengths = []
        hash = [False] * (freq + 5)
        hash[0] = True
        for i in range(len(hash)):
            if hash[i]:
                for j in a.complete_lengths:
                    if (i + j) < len(hash):
                        hash[i + j] = True
        for i in range(len(hash)):
            if hash[i]:
                c.complete_lengths.append(i)

        c.prefix_lengths = a.prefix_lengths
        c.prefix_lengths[0] = 0
        for i in c.complete_lengths:
            for j in range(len(a.prefix_lengths)):
                if (i + j) < (freq + 5):
                    c.prefix_lengths[i + j] = min(c.prefix_lengths[i + j], i + a.prefix_lengths[j], INF)

        c.suffix_lengths = a.suffix_lengths
        c.suffix_lengths[0] = 0
        for i in c.complete_lengths:
            for j in range(len(a.suffix_lengths)):
                if (i + j) < (freq + 5):
                    c.suffix_lengths[i + j] = min(c.suffix_lengths[i + j], i + a.suffix_lengths[j], INF)

        c.min_length = a.min_length
        for i in range(len(c.suffix_lengths)):
            for j in range(len(c.prefix_lengths)):
                if (i + j) >= freq:
                    c.min_length = min(c.min_length, c.suffix_lengths[i] + c.prefix_lengths[j], INF)

        return c

    for symb in exp:
        make_step(symb)

    if len(stack) > 1:
        raise AttributeError('regular expression is incorrect')

    answer = stack.pop()
    if (answer.min_length >= INF):
        print("INF")
    else:
        print(answer.min_length)


def main():
    exp, letter, freq = get_input()
    try:
        find_shortest_word(exp, letter, freq)
    except AttributeError:
        print("ERROR")

if __name__ == '__main__':
    main()
