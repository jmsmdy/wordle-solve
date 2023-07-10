from .simulator import WordleWord

def load_dictionary(source='csw2019.txt'):
    with open(source, 'r') as f:
        lines = f.read().splitlines()
    words = [
        line.strip() for line in lines
        if (' ' not in line.strip()) and len(line.strip()) > 0
    ]
    return [WordleWord(w.lower()) for w in sorted(words) if len(w) == 5]