from __future__ import print_function
import os
import subprocess
import time

main_dir = "C:/Users/herbas/Desktop/pdf"

t_start_time = time.time()

file_size_kb = 0
compressed_file_size_kb = 0
count = 0

for root, dirs, files in os.walk(main_dir):
    for file in files:
        if file.endswith(".pdf"):
            filename = os.path.join(root, file)

            print("%s sıkıştırılıyor..." % file)
            start_time = time.time()

            arg1 = '-sOutputFile=' + "compressed_" + file  # added a c to the filename
            p = subprocess.Popen(['C:/Program Files/gs/gs9.55.0/bin/gswin64c.exe', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                                 '-dPDFSETTINGS=/screen', '-dNOPAUSE', '-dBATCH', '-dQUIET', str(arg1), filename], cwd=root, stdout=subprocess.PIPE)
            print(p.communicate())

            count += 1
            compressed_file_path = os.path.join(root, "compressed_" + file)
            compressed_file_size_kb += os.path.getsize(compressed_file_path)
            file_size_kb += os.path.getsize(filename)

            os.remove(filename)
            os.rename(compressed_file_path, filename)

            print("işlem süresi:  %s saniye " %
                  ("{:.2f}".format(time.time() - start_time)))
            print("------------------------------------------")

print("Toplam işlem süresi:  %s saniye " %
      ("{:.2f}".format(time.time() - t_start_time)))

file_size_mb = "{:.2f}".format(file_size_kb / (1024*1024))
compressed_file_size_mb = "{:.2f}".format(
    compressed_file_size_kb / (1024*1024))

compress_perc = "{:.2f}".format(
    ((file_size_kb - compressed_file_size_kb) / file_size_kb) * 100)

print("Sıkıştırılan dosya: %s adet" % count)
print("Toplam boyut: %s mb" % file_size_mb)
print("Sıkıştırılmış toplam boyut: %s mb" % compressed_file_size_mb)
print("Sıkıştırma oranı: %s" % compress_perc)
