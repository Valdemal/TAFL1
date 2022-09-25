from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import List


@dataclass
class Rule:
    left: str
    right: str

    def __str__(self):
        return f'{self.left} -> {self.right}'


class Grammar:
    def __init__(self, non_terminals: List[str], terminals: List[str],
                 rules: List[Rule], start_non_terminal: str):
        self.__non_terminals = non_terminals
        self.__terminals = terminals
        self.__rules = rules
        self.__start_non_terminal = start_non_terminal

    @property
    def start_non_terminal(self) -> str:
        return self.__start_non_terminal

    @property
    def terminals(self) -> List[str]:
        return self.__terminals

    @property
    def non_terminals(self) -> List[str]:
        return self.__non_terminals

    @property
    def rules(self) -> List[Rule]:
        return self.__rules

    def is_terminal_chain(self, chain: str) -> bool:
        return all(letter in self.terminals for letter in chain)

    def start_conclusion(self, type_of_conclusion: 'Conclusion.Types') -> 'Conclusion':

        match type_of_conclusion:
            case Conclusion.Types.LEFT:
                return LeftConclusion(self)
            case Conclusion.Types.GENERAL:
                return GeneralConclusion(self)
            case _:
                raise Exception('Invalid type of conclusion!')

    def get_rules_applicable_to_chain_indices(self, chain: str) -> List[int]:

        first_terminal = next((letter for letter in chain if letter in self.non_terminals), None)

        if first_terminal is None:
            return []
        else:
            return [i for i in range(len(self.__rules)) if first_terminal == self.__rules[i].left]


class Conclusion(ABC):
    class Types(Enum):
        LEFT = auto()
        GENERAL = auto()

    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self._rules_sequence: List[int] = []

    def get_rules_sequence(self) -> List[int]:
        return self._rules_sequence

    def drop(self) -> None:
        self._rules_sequence = []

    def apply_rule_to_chain(self, rule_index: int, chain: str) -> str:
        """
        Небезопасный метод. Пользователь может передать индекс правила,
        не применимого к цепочке
        """

        rule = self._grammar.rules[rule_index]
        self._rules_sequence.append(rule_index)
        return chain.replace(rule.left, rule.right, 1)

    @abstractmethod
    def get_indices_of_rules_applicable_to_chain(self, chain: str) -> List[int]:
        pass

    @abstractmethod
    def apply_rules(self, rules_indeces_sequece: List[int]) -> str or None:
        """
        Возвращает терминальную цепочку, если применив(к начальному нетерминалу)
        по порядку i-е правила грамматики из последавательности номеров правил,
        можно получить терминальную цепочку, иначе None.

        :argument Последовательность индексов правил грамматики.
        :return Терминальная цепочка или None.
        """
        pass

    def build_tree(self) -> str:
        """Работает для левого, а по идее должно для всех"""
        tree_stack = [self._grammar.start_non_terminal, ]
        res = []

        for rule_index in self._rules_sequence:
            self.__building_tree_step(rule_index, res, tree_stack)

        while len(tree_stack):
            res.append(tree_stack.pop())

        return ''.join(res)

    def __building_tree_step(self, rule_index: int, res: List[str], tree_stack: List[str]):
        # Пока элемент стека терминал или скобка
        while tree_stack[-1] not in self._grammar.non_terminals:
            res.append(tree_stack.pop())

        res.append(tree_stack.pop())

        tree_stack.append(')')

        for letter in reversed(self._grammar.rules[rule_index].right):
            tree_stack.append(letter)

        tree_stack.append('(')


class LeftConclusion(Conclusion):
    def get_indices_of_rules_applicable_to_chain(self, chain: str) -> List[int]:
        first_terminal = self.__get_first_terminal(chain)

        return [
            i for i in range(len(self._grammar.rules))
            if first_terminal == self._grammar.rules[i].left
        ]

    def apply_rules(self, rules_indeces_sequece: List[int]) -> str or None:
        self.drop()
        current_chain = self._grammar.start_non_terminal

        for rule_index in rules_indeces_sequece:
            first_terminal = self.__get_first_terminal(current_chain)

            if first_terminal is None or self._grammar.rules[rule_index].left != first_terminal:
                return None
            else:
                current_chain = self.apply_rule_to_chain(rule_index, current_chain)

        return current_chain \
            if self._grammar.is_terminal_chain(current_chain) else None

    def __get_first_terminal(self, current_chain) -> str or None:
        return next(
            (letter for letter in current_chain if letter in self._grammar.non_terminals),
            None
        )


class GeneralConclusion(Conclusion):
    def get_indices_of_rules_applicable_to_chain(self, chain: str) -> List[int]:
        non_terminals = list(
            filter(lambda letter: letter in self._grammar.non_terminals, chain)
        )

        return list(set([
            i for i in range(len(self._grammar.rules))
            if self._grammar.rules[i].left in non_terminals
        ]))

    def apply_rules(self, rules_indeces_sequece: List[int]) -> str or None:
        self.drop()
        current_chain = self._grammar.start_non_terminal

        for rule_index in rules_indeces_sequece:
            non_terminal = self._grammar.rules[rule_index].left

            if non_terminal in current_chain:
                current_chain = self.apply_rule_to_chain(rule_index, current_chain)
            else:
                return None

        return current_chain \
            if self._grammar.is_terminal_chain(current_chain) else None
