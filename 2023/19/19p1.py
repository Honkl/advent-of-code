from typing import Union, Dict


class Part:
    items: Dict[str, int]

    def __init__(self, line: str) -> None:  # noqa
        value = line.replace("{", "").replace("}", "")
        self.items = {}
        for item in value.split(","):
            variable, value = item.split("=")
            self.items[variable] = int(value)

    def __str__(self) -> str:
        return str([f"{k}={v}" for k, v in self.items.items()])

    def rating(self) -> int:
        return sum(self.items.values())


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

    def eval(self, part: Part) -> str:
        for k, v in part.items.items():
            if k == self.variable:
                if self.operator == "<":
                    if v < self.value:
                        return self.result_true
                    else:
                        return self.result_false
                if self.operator == ">":
                    if v > self.value:
                        return self.result_true
                    else:
                        return self.result_false

        raise ValueError


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

    def eval(self, part: Part) -> str:
        result = self.condition.eval(part)

        while result not in ["A", "R"]:

            # We have another sub-condition
            if isinstance(result, Condition):
                result = result.eval(part)

            # We have reference to completely different rule
            else:
                result = ruleset[result].eval(part)

        return result


if __name__ == '__main__':
    ruleset = {}
    parts = []

    is_rule = True
    with open("input.txt", "r") as f:
        for line in f:
            if line.strip() == "":
                is_rule = False
                continue
            if is_rule:
                r = Rule(line)
                ruleset[r.name] = r
            else:
                parts.append(Part(line))

    total = 0
    for p in parts:
        if ruleset["in"].eval(p) == "A":
            total += p.rating()

    print(total)
