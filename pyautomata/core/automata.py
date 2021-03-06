"""
The class that controls the whole Automata.
The Minimized version is on the minimizaiton module.
"""
from typing import List, Dict, Tuple, Union, Set
import re


class Automata:
    """
    The class that represents an Automata
    """

    def __init__(
        self, program_function: Dict[Tuple[str, str], str], **kwargs
    ) -> None:
        """
        To initialize an Automata, pass the program function dictionary
        and the unpacked dictionary of info
        """
        self.name: str = kwargs["name"]
        self.states: Set[str] = kwargs["states"]
        self.alphabet: Set[str] = kwargs["alphabet"]
        self.initial_state: str = kwargs["initial_state"]
        self.final_states: Set[str] = kwargs["final_states"]
        self.program_function: Dict[Tuple[str, str], str] = program_function

    def break_word(self, word: str) -> List[str]:
        """
        Breaks a word into it's alphabet elements
        Will raise ValueError if there's an element
        that isn't part of the alphabet
        """
        re_pattern = "|".join(self.alphabet)
        if re.sub(re_pattern, "", word):
            raise ValueError("Word contains non-alphabet characters")
        return re.findall(re_pattern, word)

    def check_word(self, word: str) -> Tuple[bool, Union[str, List[str]]]:
        """
        Checks if a word is part of the language.
        Returns True or False, in case of True, with the second element of
        the tuple representing the path it took to reach the final state
        In case of False, the second element is the reason why it was rejected
        """
        curr_state = self.initial_state
        path = [curr_state]
        for elem in self.break_word(word):
            path.append(elem)
            try:
                curr_state = self.program_function[(curr_state, elem)]
            except KeyError:
                return_string = "Program ended with undefined state at state"
                return (
                    False,
                    f"{return_string} {curr_state} with element {elem}.",
                )
            path.append(curr_state)
        if curr_state not in self.final_states:
            return (False, f"Program ended on non-final state {curr_state}.")
        return (True, path)

    def __str__(self) -> str:
        return_string = f"{self.name}=("
        return_string += f"{self.states},{self.alphabet},Prog,"
        return_string += f"{self.initial_state},{self.final_states})\nProg\n"
        for (i_state, c), f_state in self.program_function.items():
            return_string += f"({i_state},{c})={f_state}\n"
        return return_string
