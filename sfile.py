f = open('newfile',"wb")
f.seek(1024**2-6)
f.write(b'hamada')
f.close()
import os
size = os.stat("newfile").st_size
print(size)


import hashlib
result = hashlib.md5(b"newfile")
print(result.digest())