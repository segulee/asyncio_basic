import time
import asyncio
import concurrent.futures


def run2(*args):
    print("run2: {}".format(args[1] - args[0]))
    time.sleep(args[2])


def run1(*args):
    print("run1: {}".format(args[1] + args[0]))
    time.sleep(args[2])


async def runners(loop, e, runs, *args):
    await loop.run_in_executor(e, runs, *args)


async def do_something_async(loop, e, i, j, sleep):
    tasks = []
    for x in range(i):
        for y in range(j):
            run = run1
            if x % 2 == 0:
                run = run2
            tasks.append(asyncio.ensure_future(runners(loop, e, run, x, y, sleep)))
    await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
workers = 6
executors = concurrent.futures.ProcessPoolExecutor(max_workers=workers)

a = b = 2
sleep = 1

start = time.time()
with executors as e:
    try:
        loop.run_until_complete(do_something_async(loop, e, a, b, sleep))
    except Exception as e:
        print(e)
    finally:
        loop.close()
print("async time taken: {}".format(time.time() - start))

start = time.time()
for x in range(a):
    for y in range(b):
        run = run1
        if x % 2 == 0:
            run = run2
        run(x, y, sleep)
print("sync time taken: {}".format(time.time() - start))
