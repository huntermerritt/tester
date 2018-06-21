import time
import asyncio
import requests

start = time.time()


def tic():
    return 'at %1.1f seconds' % (time.time() - start)


async def gr1(test):
    print('gr1 started work: {}'.format(tic()))
    start = time.time()
    temp = requests.get('http://www.google.com')
    status = temp.status_code
    end = time.time()

    retval = {"testname": test, "starttime": start, "endtime": end, "totaltime": end - start, "responsecode": status}
    return retval



ioloop = asyncio.get_event_loop()
tasks = [
    ioloop.create_task(gr1("test1")),
    ioloop.create_task(gr1("test2")),
    ioloop.create_task(gr1("test3"))
]
holder = ioloop.run_until_complete(asyncio.gather(*tasks))
print("PRINT HOLDER")
retval = {"Name": "Test Results", "Results": []}
for item in holder:
    retval["Results"].append(item)

print(retval)
ioloop.close()
