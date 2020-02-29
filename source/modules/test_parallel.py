import os
from multiprocessing import Process, current_process


def square(number):
    result = number + number
    print(f"{os.getpid()}: Num {number} squared is {result}")


if __name__ == "__main__":

    processes = []
    numbers = [1,2,3,4,5]

    for number in numbers:
        process = Process(target=square, args=(number, ))
        processes.append(process)
        process.start()


