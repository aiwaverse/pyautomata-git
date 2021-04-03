import abc
import re
from more_itertools import grouper
from typing import Dict, List, Union, Tuple


class Parser(abc.ABC):
    @abc.abstractmethod
    def parse(self):
        pass


class AutomataParser(Parser):
    def __init__(self, input_string: str) -> None:
        self._input_string = input_string

    @property
    def input_string(self) -> str:
        """
        Returns the input string
        """
        return self._input_string

    @input_string.setter
    def input_string(self, s: str) -> None:
        """
        Changes the input string for the program
        """
        self._input_string = s

    @staticmethod
    def description_parse(
        description: str,
    ) -> Dict[str, Union[str, List[str]]]:
        """
        Parses the description line
        returns a dictionary with the information
        """
        initial_description_results = re.findall(
            r"\w+(?==\()|(?<={)[\w+,]+(?=})|(?<=,)\w+(?=,)", description,
        )
        return {
            "name": initial_description_results[0],
            "states": initial_description_results[1].split(","),
            "alphabet": initial_description_results[2].split(","),
            "initial_state": initial_description_results[4],
            "final_states": initial_description_results[5].split(","),
        }

    @staticmethod
    def program_function_parse(
        program_function: str,
    ) -> Dict[Tuple[str, str], str]:
        """
        Parses the program function
        returns a dictionary that waits for a tuple as a key (state, word)
        """
        program_function_results = re.findall(
            r"(?<=\()\w+,\w+(?=\)=)|(?<==)\w+", program_function
        )
        grouped = grouper(program_function_results, 2)
        return_dict = {}
        for group in grouped:
            state, transition_word = tuple(group[0].split(","))
            return_dict.update({(state, transition_word): group[1]})
        return return_dict

    def parse(
        self,
    ) -> Tuple[Dict[str, Union[str, List[str]]], Dict[Tuple[str, str], str]]:
        """
        Run the whole parsing
        Returns 2 dictionaries: (description, program function)
        """
        split_string = self.input_string.split("\n")
        initial_description = split_string[0]
        program_function = "".join(split_string[2:])
        description_dict = self.description_parse(initial_description)
        program_dict = self.program_function_parse(program_function)
        return description_dict, program_dict