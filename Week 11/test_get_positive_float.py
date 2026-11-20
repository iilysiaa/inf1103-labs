#External code to test get_positive_float()
#input() is replaced with a fake that "types" a list of answers, so the test runs without a keyboard

import builtins
import io
from contextlib import redirect_stdout

from product import get_positive_float


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


# Run get_positive_float() with the given typed answers; return (value, printed messages, prompts asked)
def run_with_answers(answers: list) -> tuple:
    remaining = list(answers)
    prompts: list = []

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return remaining.pop(0)

    real_input = builtins.input
    builtins.input = fake_input
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            value = get_positive_float("Price: ")
    finally:
        builtins.input = real_input
    return value, buffer.getvalue().splitlines(), prompts


NOT_A_NUMBER = "Please enter a valid number, e.g. 12.50"
NOT_POSITIVE = "Please enter a number greater than zero."

print("get_positive_float()")
print("-" * 45)

value, messages, prompts = run_with_answers(["12.50"])
check("valid '12.50' first time -> 12.5, asked once, no messages", value == 12.5 and len(prompts) == 1 and messages == [])

value, messages, prompts = run_with_answers(["abc", "9.99"])
check("text 'abc' -> 'valid number' message, then accepts 9.99", value == 9.99 and messages == [NOT_A_NUMBER])

value, messages, prompts = run_with_answers(["", "5"])
check("empty input -> 'valid number' message, then accepts 5", value == 5.0 and messages == [NOT_A_NUMBER])

value, messages, prompts = run_with_answers(["0", "-3", "1"])
check("0 and -3 -> 'greater than zero' twice, then accepts 1", value == 1.0 and messages == [NOT_POSITIVE, NOT_POSITIVE])

value, messages, prompts = run_with_answers(["nan", "inf", "-inf", "20"])
check("'nan', 'inf' and '-inf' are rejected as not valid numbers, then accepts 20",
      value == 20.0 and messages == [NOT_A_NUMBER, NOT_A_NUMBER, NOT_A_NUMBER])

value, messages, prompts = run_with_answers(["  7.5  ", "1e2"])
check("spaces around a number are fine: '  7.5  ' -> 7.5", value == 7.5)

value, messages, prompts = run_with_answers(["twelve", "0", "-1", "3.25"])
check("mixed bad inputs -> asks 4 times in total, returns 3.25", value == 3.25 and len(prompts) == 4)
check("the same prompt is shown every time", prompts == ["Price: "] * 4)
check("returns a float", isinstance(value, float))
