# This is a sample Python script.
import concurrent.futures
import sys
import threading
import time
import  uuid
from pprint import pp
import urllib
import words
MAX_PROCESSING_LENGTH = 3
QUEUE = {}
CURRENT_PROCESS = {}
SUCCESS = []
FAIL = []
def read_file(file):
    # f = open(file, 'rt', encoding='utf-8')
    # for line in f:
    #     sys.stdout.write(line)
    # f.close()
    # Don't have to call close() explicitly when using 'with'
    with open(file, 'rt', encoding='utf-8') as f:
        for line in f:
            sys.stdout.write(line)


def func():
    pass


class Car:
    """CAR CLASS"""

    def __init__(self, number): # not a constructor btw, its an initializer
        if len(str(number)) < 3:
            raise ValueError(f'Number too short')
        # if not number.isdigit(): # AttributeError: 'int' object has no attribute 'isdigit'
        #     raise ValueError(f'Not a valid number')
        self._number = number # underscore name to avoid variable name clash

    def number(self):
        return self._number


def the_thread_function(processId, obj):
    print(f"{processId}, {obj}")
    # createNewProcess = SomeData(arg)
    if obj._kill == True:
        print(f"Killing process {obj._uuid} for file {obj._name}")
        FAIL.append(obj._name)
        CURRENT_PROCESS.pop(obj._uuid)
        if len(QUEUE) > 0:
            proc = next(iter(QUEUE.items()))[1]
            QUEUE.pop(proc._uuid)
            print("ADD MOR", proc)
            CURRENT_PROCESS[proc._uuid] = proc
        return
    print(f'Starting process {processId} for file {obj._name}')
    time.sleep(1)
    print(f'Stopping {processId} for file {obj._name}')
    SUCCESS.append(obj._name)
    CURRENT_PROCESS.pop(processId)
    pp(CURRENT_PROCESS)
    if len(QUEUE) > 0 and len(CURRENT_PROCESS) < MAX_PROCESSING_LENGTH:
        proc = next(iter(QUEUE.items()))[1]
        QUEUE.pop(proc._uuid)
        print("ADD MOR", proc)
        CURRENT_PROCESS[proc._uuid] = proc
    return "PROCESS COMPLETE"

def FillProcessAndQueue(total):
    x = range(total)
    for i in x:
        idd = uuid.uuid4()
        toKillOrNotToKill = True if i % 2 == 0 else False
        obj = SomeData(f"aName{i}", idd, toKillOrNotToKill)
        if len(CURRENT_PROCESS) < MAX_PROCESSING_LENGTH:
            CURRENT_PROCESS[idd] = obj
        else:
            QUEUE[idd] = obj

def generator_function():
    """DOCSTRINGS BABYYY!!!!"""
    yield 1
    yield 2
    yield 3

class SomeData:
    def __init__(self, name, id, kill):
        self._name = name
        self._uuid = id
        self._kill = kill

    def __repr__(self):
        """BING BONG"""
        rep = 'SomeData(' + str(self._uuid) + ',' + str(self._name) + ',' + str(self._kill)+')'
        return rep

    @property
    def getId(self):
        return self._uuid

def create_threads():
    for key, value in CURRENT_PROCESS.items():
        x = threading.Thread(target=the_thread_function, args=(key, value,))

    # for key, value in CURRENT_PROCESS.items():
    #     print(f"Key: {key} Value: {value._name}")
    # raise_exception('k')


def raise_exception(letter):
    try:
        int(letter)
    except (KeyError, TypeError) as e:
        print(f'KeyError/TypeError: {e!r}', file=sys.stderr)
    except ValueError as e:
        print(f'ValueError: {e!r}', file=sys.stderr)


def list_comprehension(listOfWords):
    return [len(word) for word in listOfWords]


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def use_zip():
    iterable1 = [1, 2, 3]
    iterable2 = [23, 45, 66]
    iterable3 = [4, 5, 6]
    for z in zip(iterable1, iterable3, iterable2):
        print(f'key {z}, Avg: {sum(z) / len(z):4.1f} ')


# words.words()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    FillProcessAndQueue(30)
    # create_threads()
    while len(CURRENT_PROCESS) > 0:
        proc = next(iter(CURRENT_PROCESS.items()))[1]

        t = threading.Thread(target=the_thread_function, args=(proc._uuid, proc,))
        t.run()

        print('COUNT',threading.activeCount())
        # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        #     print("POOL")
        #     executor.map(the_thread_function, CURRENT_PROCESS)

        print(f"Currently processing: {len(CURRENT_PROCESS)}")
        print(f"In Queue: {len(QUEUE)}")
    print('SUCCESSSS', SUCCESS)
    print('FAIL', FAIL)
    print('\n')
    print('THREADS LEFT?>')
    for thread in threading.enumerate():
        print(thread.name)
    # while len(QUEUE) > 0:
    #     print('')
    # print()
    # read_file('test.txt')
    # print_hi('PyCharm')
    # use_zip()
    # g1 = generator_function()
    # g2 = generator_function()
    # pp(next(g1))
    # pp(next(g2))
    # pp(next(g1))
    # pp(next(g2))
    # pp(next(g1))
    # pp(next(g2))
    # result = list_comprehension(['Fever', '333'])
    # pp(result)
    # c = Car(123)
    # pp(c.number())
    # create_threads()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
