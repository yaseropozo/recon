import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from threading import Thread
import time
import requests
import sys
import os.path

def usage():
    print("----------USAGE INSTRUCTION ---------")
    print(f"{sys.argv[0]} URL_LIST_FILE WORDLIST NUMBER_OF_THREADS(Default is 10)\n")
    sys.exit()

def prepare(myList, numOfChunks):
    for i in range(0, len(myList), numOfChunks):
        yield myList[i:i + numOfChunks]

def brute(myList, wordlist, numOfThreads):
    start = time.perf_counter()
    for lists in myList:
        threads.append(Thread(target=worker, args=(lists, wordlist), daemon=True))
    for thread in threads:
        try:
            thread.start()
        except KeyboardInterrupt:
            print("\nReceived Keyboard Interrupt  , Terminating threads\n")
            sys.exit()
    for thread in threads:
        try:
            thread.join()
        except KeyboardInterrupt:
            print("\nReceived Keyboard Interrupt  , Terminating threads\n")
            sys.exit()
    finish = time.perf_counter()
    print(f"\n\n\t\t Checked {total_len} Directories in {round(finish-start,2)} Seconds\n")

def worker(lists, wordlist):
    try:
        for word in lists:
            if word.startswith("/"):
                word = word[1:]
            for url in urls:
                url = url.strip()
                url2 = url + "/" + word.strip()
                try:
                    r = requests.get(url2, verify=False)
                    if str(r.status_code) in match:
                        print(f"{url2},{r.status_code},{len(r.content)}")
                except requests.RequestException as e:
                    pass
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        sys.exit()

if __name__ == "__main__":
    try:
        match = ['200', '301', '302', '401', '403', '429']  # change this to filter responses
        try:
            if sys.argv[1]:
                url_list_file = sys.argv[1]
            if sys.argv[2]:
                wordlist = sys.argv[2]
            try:
                if sys.argv[3]:
                    numOfThreads = int(sys.argv[3])
            except:
                numOfThreads = 10
        except:
            usage()
        if os.path.isfile(url_list_file) == False:
            print(f"The file {url_list_file} doesn't exist")
            sys.exit()

        with open(url_list_file, 'r') as url_file:
            urls = url_file.readlines()

        if os.path.isfile(wordlist) == False:
            print(f"The file {wordlist} doesn't exist")
            sys.exit()

        with open(wordlist, 'r') as w:
            myList = w.readlines()
        total_len = len(myList)
        final = []
        threads = []
        if numOfThreads > total_len or numOfThreads < 0:
            print("\nToo High Value for Threads with Respect to Input Word-list\n")
            sys.exit(1)
        numOfChunks = len(myList) // numOfThreads
        myList_new = prepare(myList, numOfChunks)
        brute(myList_new, wordlist, numOfThreads)
    except KeyboardInterrupt:
        sys.exit()
