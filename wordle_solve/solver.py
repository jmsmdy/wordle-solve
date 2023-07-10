from typing import Sequence
from .simulator import WordleWord, WordContainsConstraint, LetterPositionConstraint, WordleSimulator

class ConstraintSolver:
    def __init__(self, dictionary: Sequence[WordleWord]):
        self.dictionary = dictionary

    def find_all_solutions(self, constraints: Sequence[WordContainsConstraint | LetterPositionConstraint]) -> list[WordleWord]:
        matches = self.dictionary
        for constraint in constraints:
            matches = [w for w in matches if constraint.satisfies(w)]

        return matches
    
    def strategically_guess(self, ws: WordleSimulator, max_guesses=100):
        if len(ws.guesses) == 0:
            best_next_guess =  WordleWord('maker')
        else:
            possible_solutions = self.find_all_solutions(ws.constraints())
            tuned_cs = ConstraintSolver(possible_solutions)
            # limit guesses for performance reasons
            overpopulation_factor = max(1, (len(possible_solutions) // max_guesses))
            next_guesses_to_evaluate = [x for i, x in enumerate(possible_solutions) if (i % overpopulation_factor) == 0]
            guess_evaluations = []
            for next_guess in next_guesses_to_evaluate:
                one_step_simulators = [
                    WordleSimulator(possible_solution)
                    for possible_solution in possible_solutions
                ]
                for simulator in one_step_simulators:
                    #for old_guess in ws.guesses:
                    #    simulator.guess(old_guess)
                    simulator.guess(next_guess)
                guess_evaluations.append([
                    len(tuned_cs.find_all_solutions(simulator.constraints()))
                    for simulator in one_step_simulators
                ])
            best_next_guess_index = sorted(enumerate(guess_evaluations), key=lambda x: (max(x[1]), sum(x[1]) / len(x[1])))[0][0]
            best_next_guess = next_guesses_to_evaluate[best_next_guess_index]
        print('Next guess:', best_next_guess)
        return best_next_guess