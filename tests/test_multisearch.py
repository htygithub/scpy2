from os import path
import re
from scpy2.cython import MultiSearch

with open(path.join(path.dirname(__file__), "english_text.txt"), "rb") as f:
    text = f.read()


def make_words(n):
    words = list(set(re.findall(r"\w+", text)))[:n]
    _words = ",".join(words)
    words = [word for word in words if _words.count(word) == 1]
    return words


def plain_search(words, text):
    results = []
    for word in words:
        pos = 0
        while True:
            pos = text.find(word, pos)
            if pos != -1:
                results.append((pos, word))
                pos += 1
            else:
                break
    results.sort()
    return results


def multi_search(words, text, ms=None):
    if ms is None:
        ms = MultiSearch(words)
    results = []

    def callback(pos, word):
        results.append((pos, word))
        return False

    ms.search(text, callback)
    results.sort()
    return results


def multi_iter_search(words, text, ms=None):
    if ms is None:
        ms = MultiSearch(words)
    results = list(ms.iter_search(text))
    results.sort()
    return results


def test_search():
    for n in range(1, 200):
        words = make_words(n)
        res1 = plain_search(words, text)
        res2 = multi_search(words, text)
        assert res1 == res2


def test_isin():
    for n in range(1, 200):
        words = make_words(n)
        ms = MultiSearch(words)
        assert ms.isin(text) == True

    ms = MultiSearch(["XXXX", "YYYY"])
    assert ms.isin(text) == False


def test_search_twice():
    for n in range(1, 200):
        words = make_words(n)
        ms = MultiSearch(words)
        res1 = multi_search(None, text, ms)
        res2 = multi_search(None, text, ms)
        assert res1 == res2


def test_iter_search():
    for n in range(1, 200):
        words = make_words(n)
        res1 = multi_search(words, text)
        res2 = multi_iter_search(words, text)
        assert res1 == res2


if __name__ == '__main__':
    test_search()
    test_isin()
    test_search_twice()
    test_iter_search()