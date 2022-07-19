import os, time, sys

paths = [r"D:\Python projects\QR\JSON files",
         r"D:\Python projects\QR\data"]
now = time.time()

# for f in os.listdir(path):
#     if 'media' in os.listdir(os.path.join(path,f)):
#
#         print('yes')

for path in paths:
    for f in os.listdir(path):
        f = os.path.join(path,f)
        if os.stat(f).st_mtime > now - 7 * 86400:
