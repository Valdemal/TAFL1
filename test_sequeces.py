from config import my_grammar, toolkit_grammar
from grammar import Conclusion

sequences = [
    [0, 2, 3, 4, 6, 1, 6, 4, 6],
    [0, 0, 1, 6, 4, 6, 2, 1, 6],
    [0, 4, 6, 2, 3, 1, 6, 4, 6],
    [0, 2, 0, 4, 1, 1, 6, 6, 6]
]


def print_conclusion(conclusion_type: Conclusion.Types):
    match conclusion_type:
        case Conclusion.Types.LEFT:
            print('Левый вывод:')
        case Conclusion.Types.GENERAL:
            print('Общий вывод:')
        case _:
            raise Exception('Неправильный тип вывода!')


if __name__ == "__main__":
    g = my_grammar

    print("Последовательности:")
    for i in range(len(sequences)):
        print(f"{i + 1}. ", end='')

        for elem in sequences[i]:
            print(elem + 1, end=' ')

        print('')

    for conclusion_type in list(Conclusion.Types):
        conclusion = g.start_conclusion(conclusion_type)
        print_conclusion(conclusion_type)

        for i in range(len(sequences)):
            flag = conclusion.apply_rules(sequences[i]) is not None
            print(f"{i + 1}. {'Можно применить' if flag else 'Нельзя применить'}")
