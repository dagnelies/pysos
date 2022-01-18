import time
import test_rnd as rnd
import random
import pysos

# initialize the data
N = 1234
items = [(rnd.utf8(20), rnd.utf8(200)) for i in range(N)]

start = time.time()

db = pysos.Dict('temp/sos_dict')

#import shelve
#db = shelve.open('temp.shelve')


print("%.2fs: %d items loaded" % (time.time() - start, len(db)))

# add all items
for key,val in items:
    db[key] = val
print("%.2fs: %d items added" % (time.time() - start, len(items)))

# read all keys
random.shuffle(items)
for key,val in items:
    val2 = db[key]
    assert val2 == val
print("%.2fs: %d items read" % (time.time() - start, len(items)))

# update all values
random.shuffle(items)
for key,val in items:
    db[key] = 'updated ' + val
print("%.2fs: %d items updated" % (time.time() - start, len(items)))

# read all keys again
random.shuffle(items)
for key,val in items:
    val2 = db[key]
    assert val2 == 'updated ' + val
print("%.2fs: %d items read" % (time.time() - start, len(items)))

# delete all keys
random.shuffle(items)
for key,val in items:
    del db[key]
print("%.2fs: %d items deleted" % (time.time() - start, len(items)))

# add all keys
random.shuffle(items)
for key,val in items:
    db[key] ='again ' + val
print("%.2fs: %d items added" % (time.time() - start, len(items)))

# read all keys again
random.shuffle(items)
for key,val in items:
    val = db[key]
print("%.2fs: %d items read" % (time.time() - start, len(items)))

N = len(db)
db.close()
print("%.2fs: DB closed containing %d item" % (time.time() - start, N))
#print("free lines: %d" % len(db._free_lines))

