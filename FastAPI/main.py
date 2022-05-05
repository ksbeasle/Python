import time
from pprint import pp
import uvicorn
import queue

from fastapi import FastAPI
import  uuid
import threading
MAX_PROCESSING_LENGTH = 3
QUEUE = {}
CURRENT_PROCESS = {}
SUCCESS = []
FAIL = []
q = queue.Queue()


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


def FillProcessAndQueue(total):
    x = range(total)
    for i in x:
        idd = uuid.uuid4()
        toKillOrNotToKill = True if i % 2 == 0 else False
        obj = SomeData(f"aName{i}", i, toKillOrNotToKill)
        if len(CURRENT_PROCESS) < MAX_PROCESSING_LENGTH:
            CURRENT_PROCESS[i] = obj
            print(CURRENT_PROCESS)
        else:
            QUEUE[i] = obj
            print(QUEUE)


def QueueTest():
    for i in range(30):
        q.put(SomeData(f"aName{i}", i, False))
    print(f"# in Q is: {q.qsize()}")


def DoWork():
    while q.qsize() > 0:
        item = q.get()
        print(f"I HAVE {item}")
        time.sleep(10)
        print(f"There are {q.qsize()} left")
        q.task_done()

    print("dasddas")
    return


# Queue Thread
threading.Thread(target=DoWork, args=(q,))

app = FastAPI()

def the_thread_function(processId, obj):
    time.sleep(2)
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


@app.get('/queue')
def BuildQueue():
    QueueTest()
    print("Done")


@app.get('/queue/start')
def StartQueue():
    DoWork()
    q.join()
    time.sleep(3)
    BuildQueue()
    return

@app.get('/show')
def Show():
    return {
        "Fail": FAIL,
        "Success": SUCCESS,
        "Current": CURRENT_PROCESS,
        "Queue": QUEUE
    }

@app.get('/cancel/{uuid}')
def cancel_proc(uuid):
    try:
        currentProc = CURRENT_PROCESS.get(int(uuid))
        procInQueue = QUEUE.get(int(uuid))
        if currentProc is None and procInQueue is None:
            return {
                "Process": None,
                "Kill": None
            }
        elif currentProc is not None:
            CURRENT_PROCESS[currentProc._uuid]._kill = True
            return {
                "Process": currentProc._uuid,
                "Kill": currentProc._kill
            }
        elif procInQueue is not None:
            QUEUE[procInQueue._uuid]._kill = True
            return {
                "Process": procInQueue._uuid,
                "Kill": procInQueue._kill
            }
        else:
            return {
                "Process": None,
                "Kill": None
            }
    except Exception as e:
        print(e)

@app.get('/process/{uuid}')
def cancel_proc(uuid):
    print('IDDDD',uuid)
    return

@app.get('/health')
def ping():
    return "pong"


def loop():
    while len(CURRENT_PROCESS) > 0:
        proc = next(iter(CURRENT_PROCESS.items()))[1]

        t = threading.Thread(target=the_thread_function, args=(proc._uuid, proc,), daemon=True)
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
    time.sleep(3)

@app.get('/start')
def Start():
    print("Seeding data")
    FillProcessAndQueue(50)
    print(CURRENT_PROCESS)
    loop()
    return {
        "success": True
    }

@app.get('/threads')
def Threads():
    return { "Threads": threading.activeCount() }



if __name__ == '__main__':
    uvicorn.run(app)


# def main():
#     print("Filling the queue")
#     FillProcessAndQueue(50)
#     print("Done")
#
#     # while True:
#     #     print('ok')
#     loop()
#
# main()

