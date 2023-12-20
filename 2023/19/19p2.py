from functools import reduce
import time
from typing import Union, Dict, List, Any


class Part:
    items: Dict[str, int]

    def __init__(self, x: int, m: int, a: int, s: int) -> None:  # noqa
        self.items = {
            "x": x,
            "m": m,
            "a": a,
            "s": s,
        }

    def __str__(self) -> str:
        return str([f"{k}={v}" for k, v in self.items.items()])


class Condition:
    variable: str
    operator: str
    value: int
    result_true: str
    result_false: str

    def __init__(
            self, condition: str, result_true: Union[str, "Condition"], result_false: Union[str, "Condition"]
    ) -> None:
        self.operator = "<" if "<" in condition else ">"
        self.variable, self.value = condition.replace("<", ">").split(">")
        self.result_true = result_true
        self.result_false = result_false

        self.value = int(self.value)

    def __str__(self) -> str:
        return f"{self.variable}{self.operator}{self.value}{self.result_true},{self.result_false}"


class Rule:
    name: str
    condition: Condition

    def __init__(self, value: str) -> None:
        name, content = value.strip().replace("}", "").split("{")
        data = content.replace(":", ",").split(",")

        c = None
        while len(data) > 0:
            if c is None:
                n1 = data.pop()
                n2 = data.pop()
                n3 = data.pop()
                c = Condition(n3, n2, n1)
            else:
                n2 = data.pop()
                n3 = data.pop()
                c = Condition(n3, n2, c)

        self.condition = c
        self.name = name


def swap_operator(o: str) -> str:
    return "<=" if o == ">" else ">="


def search_paths(condition: Condition) -> List[List[Any]]:
    success_paths = []

    current_true = (condition.variable, condition.operator, condition.value)
    current_false = (condition.variable, swap_operator(condition.operator), condition.value)

    if condition.result_true == "A":
        success_paths.append([current_true])

    if condition.result_false == "A":
        success_paths.append([current_false])

    if isinstance(condition.result_true, Condition):
        result = search_paths(condition.result_true)
        for x in result:
            success_paths.append([current_true] + x)
    else:
        if condition.result_true not in ["A", "R"]:
            result = search_paths(ruleset[condition.result_true].condition)
            for x in result:
                success_paths.append([current_true] + x)

    if isinstance(condition.result_false, Condition):
        result = search_paths(condition.result_false)
        for x in result:
            success_paths.append([current_false] + x)
    else:
        if condition.result_false not in ["A", "R"]:
            result = search_paths(ruleset[condition.result_false].condition)
            for x in result:
                success_paths.append([current_false] + x)

    return success_paths


if __name__ == '__main__':
    start = time.time()

    ruleset = {}
    is_rule = True
    with open("input.txt", "r") as f:
        for line in f:
            if line.strip() == "":
                is_rule = False
                break

            r = Rule(line)
            ruleset[r.name] = r

    min_value = 1
    max_value = 4001

    # Successful paths to the "A" state
    paths = search_paths(ruleset["in"].condition)
    print(f"Successful paths: {len(paths)}")


    def _cmp(x: int, y: int, o: str) -> bool:
        return {
            "<": x < y,
            ">": x > y,
            "<=": x <= y,
            ">=": x >= y,
        }[o]


    total = 0
    for p in paths:

        options = {
            "x": list(range(min_value, max_value)),
            "m": list(range(min_value, max_value)),
            "a": list(range(min_value, max_value)),
            "s": list(range(min_value, max_value)),
        }

        for var, op, value in p:
            options[var] = [x for x in options[var] if _cmp(x, value, op)]

        combinations = reduce(lambda x, y: x * y, [len(v) for v in options.values()])
        total += combinations

    print(f"Combinations: {total}")
    print(f"Runtime: {time.time() - start}")
