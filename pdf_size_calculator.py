from __future__ import print_function
import os

main_dir = "//depoerp/ErpDosyaDepo/TempEmployee"
file_size_kb = 0

for root, dirs, files in os.walk(main_dir):
    for file in files:
        if file.endswith(".pdf"):
            filename = os.path.join(root, file)
            file_size_kb += os.path.getsize(filename)
            print(file_size_kb)


file_size_mb = "{:.2f}".format(file_size_kb / (1024*1024))
print("toplam pdf boyutu: %s" % file_size_mb)
