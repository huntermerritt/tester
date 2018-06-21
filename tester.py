import asyncio
import time
import requests

class Tester:


    def __init__(self):
        self.jobs = []

    async def runjob(self, testname, url, timewait):

        start = time.time()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        temp = requests.get(url, headers)
        status = temp.status_code
        end = time.time()
        totals = end - start

        retval = {"testname": testname, "starttime": start, "endtime": end, "totaltime": totals,
                  "responsecode": status}
        if timewait > totals:
            time.sleep(timewait - totals)

        return retval

    def addjob(self, testname, url, timewait, iterations):

        timeperjob = float(timewait) / float(iterations)

        count = 0

        while count < int(iterations):

            self.jobs.append({ "testname": testname + str(count), "url": url, "timewait": timeperjob })
            count = count + 1


    def starttests(self):

        ioloop = asyncio.get_event_loop()

        tasks = []

        for item in self.jobs:
            tasks.append(ioloop.create_task(self.runjob(item['testname'], item['url'], item['timewait'])))

        holder = ioloop.run_until_complete(asyncio.gather(*tasks))

        retval = {}
        for item in holder:
            s = item['testname']
            result = ''.join([i for i in s if not i.isdigit()])
            if result in retval.keys():
                retval[result].append(item)
            else:
                retval[result] = [item]


        return retval

        ioloop.close()


