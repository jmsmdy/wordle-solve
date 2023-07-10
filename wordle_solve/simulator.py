from typing import Any

class WordleWord:
    def __init__(self, word: str):
        self.letters = word

    def __eq__(self, other: 'WordleWord') -> bool:
        return (
            isinstance(other, WordleWord)
            and (self.letters == other.letters)
        )
    
    def __hash__(self):
        return hash((self.letters))

    def __repr__(self) -> str:
        return f'WordleWord({repr(self.letters)})'
    
class WordContainsConstraint:
    def __init__(self, letters: str):
        self.letters = ''.join(sorted(set(letters)))

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, WordContainsConstraint)
            and (self.letters == other.letters)
        )
        
    def __hash__(self):
        return hash((self.letters))
    
    def __add__(self, other: 'WordContainsConstraint') -> 'WordContainsConstraint':
        return WordContainsConstraint(self.letters + other.letters)

    def __repr__(self) -> str:
        #occurences_repr = (
        #    f', minimum_occurences={self.minimum_occurences}'
        #    if self.minimum_occurences > 1 else ''
        #)
        return f'WordContainsConstraint({repr(self.letters)})'

    def satisfies(self, word: WordleWord) -> bool:
        return  all(letter in word.letters for letter in self.letters)
    
class WordOmitsConstraint:
    def __init__(self, letters: str):
        self.letters = ''.join(sorted(set(letters)))

    def __geq__(self, other: 'WordOmitsConstraint') -> bool:
        set(self.letters).issuperset(set(other.letters))

    def __leq__(self, other: 'WordOmitsConstraint') -> bool:
        set(self.letters).issubset(set(other.letters))

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, WordOmitsConstraint)
            and (self >= other) and (other >= self)
        )
    
    def __add__(self, other: 'WordOmitsConstraint'):
        return WordOmitsConstraint(self.letters + other.letters)
        
    def __hash__(self):
        return hash((self.letters,))

    def __repr__(self) -> str:
        return f'WordOmitsConstraint({repr(self.letters)})'

    def satisfies(self, word: WordleWord) -> bool:
        return all(letter not in word.letters for letter in self.letters)
        
class LetterPositionConstraint:
    def __init__(self, letter: str, position: int):
        self.letter = letter
        self.position = position

    def __eq__(self, other: Any) -> bool:
        try:
            return (
                isinstance(other, LetterPositionConstraint)
                and (self.letter == other.letter)
                and (self.position == other.position)
            )
        except:
            return False
        
    def __hash__(self):
        return hash((self.letter, self.position))

    def __repr__(self) -> str:
        return f'LetterPositionConstraint({repr(self.letter)}, {self.position})'

    def satisfies(self, word: WordleWord) -> bool:
        return word.letters[self.position] == self.letter
    
class NotLetterPositionConstraint:
    def __init__(self, letter: str, position: int):
        self.letter = letter
        self.position = position

    def __eq__(self, other: Any) -> bool:
        try:
            return (
                isinstance(other, NotLetterPositionConstraint)
                and (self.letter == other.letter)
                and (self.position == other.position)
            )
        except:
            return False
        
    def __hash__(self):
        return hash((self.letter, self.position))

    def __repr__(self) -> str:
        return f'NotLetterPositionConstraint({repr(self.letter)}, {self.position})'

    def satisfies(self, word: WordleWord) -> bool:
        return word.letters[self.position] != self.letter
    
class WordleSimulator:
    def __init__(self, target: WordleWord):
        self.target_word = target.letters
        self.guesses = []
        self._omits = WordOmitsConstraint('')
        self._contains = WordContainsConstraint('')
        self._position_constraints = []
        self.solved = False

    def _add_new_constraints(self, guess_word: str):
        new_constraints = []
        matched_letters = {}
        mismatched_letters = {}
        for i, letter in enumerate(guess_word):
            if letter in self.target_word:
                if self.target_word[i] == letter:
                    matched_letters[letter] = matched_letters.get(letter, []) + [i]
                else:
                    matched_letters[letter] = matched_letters.get(letter, [])
                    mismatched_letters[letter] = mismatched_letters.get(letter, []) + [i]
            else:
                self._omits += WordOmitsConstraint(letter)
        self._contains += WordContainsConstraint(matched_letters.keys())
        for letter, matches in matched_letters.items():
            new_constraints += [LetterPositionConstraint(letter, i) for i in matches]
        for letter, mismatches in mismatched_letters.items():
            new_constraints += [NotLetterPositionConstraint(letter, i) for i in mismatches]
        for new_constraint in new_constraints:
            if new_constraint not in self._position_constraints:
                self._position_constraints.append(new_constraint)

    def constraints(self):
        return [self._omits, self._contains] + self._position_constraints

    def guess(self, word: WordleWord):
        self.guesses.append(word)
        self._add_new_constraints(word.letters)
        correct = (word.letters == self.target_word)
        self.solved = correct
        return correct