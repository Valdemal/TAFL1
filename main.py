from grammar import Conclusion
from config import my_grammar, toolkit_grammar


def choose_conclusion() -> Conclusion.Types:
    print("Какой вывод использовать?")
    print("1. Левый")
    print("2. Общий")

    while True:
        choice = int(input("Ваш выбор:"))
        match choice:
            case 1:
                return Conclusion.Types.LEFT
            case 2:
                return Conclusion.Types.GENERAL
            case _:
                print("Неверный ввод!")


if __name__ == '__main__':
    g = my_grammar

    conclusion = g.start_conclusion(choose_conclusion())

    current_chain = g.start_non_terminal
    applicable_rules = conclusion.get_indices_of_rules_applicable_to_chain(current_chain)

    while len(applicable_rules):
        print('Промежуточная цепочка:', current_chain)
        print('Можно применить:')

        for rule_index in applicable_rules:
            print(f'{rule_index + 1}. {g.rules[rule_index]}')

        applicable_rule_index = int(input("Применяем правило:")) - 1

        current_chain = conclusion.apply_rule_to_chain(applicable_rule_index, current_chain)
        applicable_rules = conclusion.get_indices_of_rules_applicable_to_chain(current_chain)

    print('Терминальная цепочка:', current_chain)
    print('Последовательность правил:', end=' ')

    for rule_index in conclusion.get_rules_sequence():
        print(rule_index + 1, end=' ')

    print()
    print('Дерево вывода:', conclusion.build_tree())
