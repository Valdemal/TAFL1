from grammar import Grammar, Rule, Conclusion

toolkit_grammar = Grammar(
    terminals=['a', 'b', 'c', ''],
    non_terminals=['S', 'A', 'B'],
    start_non_terminal='S',
    rules=[
        Rule('S', 'aAbS'),
        Rule('S', 'b'),
        Rule('A', 'SAc'),
        Rule('A', '')
    ]
)
my_grammar = Grammar(
    terminals=['a', 'b'],
    non_terminals=['S', 'A', 'B'],
    start_non_terminal='S',
    rules=[
        Rule('S', 'aSbA'),
        Rule('S', 'aB'),
        Rule('S', 'A'),
        Rule('A', 'aAbS'),
        Rule('A', 'aB'),
        Rule('A', 'S'),
        Rule('B', 'b'),
        Rule('B', 'aA')
    ],
)


