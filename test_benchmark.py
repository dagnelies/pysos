import pysos
import time

N = 100 * 1000

db = pysos.Dict("temp/test.db")

t = time.time()
for i in range(N):
    db["key_" + str(i)] = {"some": "object_" + str(i)}
dt = time.time() - t

print(f'Writes: {int(N / dt)} / second')

t = time.time()
for i in range(N):
    value = db["key_" + str(i)]
dt = time.time() - t
print(f'Reads: {int(N / dt)} / second')

db.close()