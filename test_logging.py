import pysos
import logging

logger = logging.getLogger('pysos')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
#logging.info('Ho?')
#logger.info('Ho?')

N = 100

db = pysos.Dict("temp/test.db")

for i in range(N):
    db["key_" + str(i)] = {"some": "object_" + str(i)}

for i in range(N):
    value = db["key_" + str(i)]

db.close()