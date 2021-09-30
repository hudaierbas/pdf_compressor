from __future__ import print_function
import os
import subprocess
import time
import sys
import signal
from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
log = open("%s.txt" % date, "w")

main_dir = "\\\\depoerp\\\\ErpDosyaDepo\\\\TempEmployee"
start_folder = sys.argv[1]  # start folder number
end_folder = sys.argv[2]  # end folder number
last_folder = ""
last_file = ""


# region log
log.write("------------------------------------------\n")
log.write("date: %s \n" % date)
log.write("main_dir: %s \n" % main_dir)
log.write("start_folder: %s \n" % start_folder)
log.write("end_folder: %s \n" % end_folder)
log.write("------------------------------------------\n")
# endregion

t_start_time = time.time()

file_size_kb = 0
compressed_file_size_kb = 0
count = 0


def handler(signum, frame):
    print("------------------------------------------")
    print("Sıkıştırma yapılan son")
    print("Klasör: ", last_folder)
    print("Dosya: ", last_file)

    # region log
    log.write("------------------------------------------\n")
    log.write("last_compress_folder: %s \n" % last_folder)
    log.write("last_compressed_file: %s \n" % last_file)
    log.write("sıkıştırma durduruldu \n")
    log.write("------------------------------------------\n")
    # endregion

    sys.exit("Sıkıştırma durduruldu.")


signal.signal(signal.SIGINT, handler)

for root, dirs, files in os.walk(main_dir):
    for file in files:
        if file.endswith(".pdf"):
            filename = os.path.join(root, file)
            folder = os.path.basename(os.path.dirname(filename))

            if int(folder) < int(start_folder) or int(folder) > int(end_folder):
                break

            last_folder = folder

            print("Klasör: %s" % folder)
            print("%s sıkıştırılıyor..." % file)
            start_time = time.time()

            arg1 = '-sOutputFile=' + "compressed_" + file
            p = subprocess.Popen(['C:/Program Files/gs/gs9.55.0/bin/gswin64c.exe', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                                 '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dBATCH', '-dQUIET', str(arg1), filename], cwd=root, stdout=subprocess.PIPE)
            print(p.communicate())

            count += 1
            compressed_file_path = os.path.join(root, "compressed_" + file)
            compressed_file_size_kb += os.path.getsize(compressed_file_path)
            file_size_kb += os.path.getsize(filename)

            os.remove(filename)
            os.rename(compressed_file_path, filename)

            last_file = file

            # region log
            log.write("------------------------------------------\n")
            log.write("last_compress_folder: %s \n" % last_folder)
            log.write("last_compressed_file: %s \n" % last_file)
            log.write("------------------------------------------\n")
            # endregion

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

# region log
log.write("------------------------------------------\n")
log.write("Sıkıştırılan dosya: %s adet \n" % count)
log.write("Toplam boyut: %s mb \n" % file_size_mb)
log.write("Sıkıştırılmış toplam boyut: %s mb \n" % compressed_file_size_mb)
log.write("Sıkıştırma oranı: %s \n" % compress_perc)
log.write("------------------------------------------ \n")
# endregion
