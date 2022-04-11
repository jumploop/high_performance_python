import multiprocessing
# python -m timeit -s "import ex2_lock_rawvalue" "ex2_lock_rawvalue.run_workers()"
# 18.5ms (slightly faster?)
# 5ms  lock.acquire
# 11ms with lock


def work(value, max_count, lock):
    for _ in range(max_count):
        with lock:
            value.value += 1
        #lock.acquire()
        #value.value += 1
        #lock.release()


def run_workers():
    NBR_PROCESSES = 4
    MAX_COUNT_PER_PROCESS = 1000
    total_expected_count = NBR_PROCESSES * MAX_COUNT_PER_PROCESS
    processes = []
    lock = multiprocessing.Lock()
    value = multiprocessing.RawValue('i', 0)
    for _ in range(NBR_PROCESSES):
        p = multiprocessing.Process(target=work, args=(value, MAX_COUNT_PER_PROCESS, lock))
        p.start()
        processes.append(p)

    # wait for the processes to finish
    for p in processes:
        p.join()

    # print the final value
    print(f"Expecting to see a count of {total_expected_count}")
    print(f"We have counted to {value.value}")


if __name__ == "__main__":
    run_workers()
