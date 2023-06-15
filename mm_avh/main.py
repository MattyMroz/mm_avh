from utils.execution_timer import ExecutionTimer

from time import sleep


def calculate_sum(upper_limit: int) -> int:
    """
    Calculates the sum of integers from 1 to n.
    """

    sum_result = 0
    for i in range(1, upper_limit + 1):
        sum_result += i
        sleep(.5)  # Simulating a time-consuming operation
    return sum_result


def main():
    """
    Main function to execute the code block with the Timer context manager.
    """

    sum_result = calculate_sum(1)
    print(f'Sum of 1..1000 = {sum_result}')


if __name__ == '__main__':
    with ExecutionTimer():
        main()
