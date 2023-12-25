from typing import Optional, List, Tuple, Dict
import math


class Module:
    type: Optional[str]
    name: str
    outputs: List[str]
    state: Optional[str]
    sources: Dict[str, str]

    def __init__(self, data: str) -> None:
        in_, out_ = data.split("->")
        in_ = in_.strip()
        self.state = None

        if "%" in in_ or "&" in in_:
            self.name = in_[1:]
            self.type = in_[0]

            if self.type == "%":
                self.state = "off"

        else:
            self.name = in_
            self.type = None

        self.outputs = []
        for value in out_.split(","):
            self.outputs.append(value.strip())

    def receive(self, value: str, source: str) -> List[Tuple[str, str]]:
        # print(f"{source} -> {value} -> {self.name}")

        if self.type == "%":
            if value == "high":
                return []

            new_signal = "high" if self.state == "off" else "low"
            self.state = "off" if self.state == "on" else "on"

        elif self.type == "&":
            self.sources[source] = value
            if all(x == "high" for x in self.sources.values()):
                new_signal = "low"
            else:
                new_signal = "high"

        elif self.type is None:
            new_signal = value

        return [(name, new_signal, self.name) for name in self.outputs]  # noqa

    def update_sources(self, all_modules: List["Module"]) -> None:
        self.sources = {}
        for m in all_modules:
            if self.name in m.outputs:
                self.sources[m.name] = "low"

    def __str__(self) -> str:
        return f"Module(name={self.name}, type={self.type}, outputs={self.outputs})"

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        modules = [Module(line) for line in f]

    for m in modules:
        m.update_sources(modules)

    config = {
        module.name: module for module in modules
    }

    # We will evaluate when these modules (i.e. modules that go to final 'rx') will become high signal
    targets = ["cl", "tn", "bm", "dr"]

    counts = {name: 0 for name in targets}
    presses = 0
    while any(v == 0 for v in counts.values()):
        queue = [("broadcaster", "low", None)]
        presses += 1
        while len(queue) > 0:
            name, signal, origin = queue.pop(0)

            # Untyped modules, skipping
            if name not in config.keys():
                continue

            if origin in targets and signal == "high" and counts[origin] == 0:
                counts[origin] = presses

            new_signals = config[name].receive(signal, origin)
            queue.extend(new_signals)

    print(counts)
    print(f"Total: {math.lcm(*counts.values())}")
