digits = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
}


def extract_advanced(value: str) -> int:
    forward_index = len(value) + 1
    forward_value = None

    backward_index = len(value) + 1
    backward_value = None

    for str_digit, int_digit in digits.items():

        for digit in [str_digit, int_digit]:
            i = value.find(digit)

            if i != -1 and i < forward_index:
                forward_index = i
                forward_value = int_digit

        for digit in ["".join(reversed(str_digit)), int_digit]:
            i = "".join(reversed(value)).find(digit)
            if i != -1 and i < backward_index:
                backward_index = i
                backward_value = int_digit

    output = f"{forward_value}{backward_value}"
    return int(output)


if __name__ == '__main__':
    total = 0
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            total += extract_advanced(line.strip())

    print(total)
