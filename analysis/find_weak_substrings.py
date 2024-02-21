import time
import json

def load_data(filepath):
    data = None
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except:
        time.sleep(1.1)
        with open(filepath, 'r') as f:
            data = json.load(f)
    return data

def find_weak_substrings():
    
    min_length = 5

    userdata = load_data('userdata.json')
    failwords = userdata["fail_words"]

    errordict = {}

    for wordinfo in failwords.values():
        for fail in wordinfo:
            string_index_start = max(0, fail["index"]-4)
            string_index_end = fail["index"]
            if string_index_end == 0:
                string_index_end = 1

            fail_substring = fail["word"][string_index_start:string_index_end]

            if fail_substring not in errordict:
                errordict[fail_substring] = 1
            else:
                errordict[fail_substring] += 1

    errorsubstrings = {}
    errorwords = []
    sorted_items = sorted(errordict.items(), key=lambda x: x[1], reverse=True)
    for item in sorted_items:
        substr = item[0]
        if len(substr) >= 2:
            #print(item)
            for i in range(0,item[1]):
                for ii in range(0, len(substr)-1):
                    spaces = " " * (len(substr) - 2 - ii)
                    rawerror = substr[ii] + spaces + substr[len(substr)-1]
                    #print(rawerror)
                    if rawerror not in errorsubstrings:
                        errorsubstrings[rawerror] = 1
                    else:
                        errorsubstrings[rawerror] += 1

    sorted_items = sorted(errorsubstrings.items(), key=lambda x: x[1], reverse=True)

    returndata = []

    for item in sorted_items:
        if item[1] >= min_length:
            #print('{:>4}'.format(item[0].replace(' ', '_')), item[1])
            returndata.append({
                "substring": item[0], 
                "freq": item[1]
            })

    return returndata


# Just here so when I run it I can observe
find_weak_substrings()