# download Ghostscript https://www.ghostscript.com/download.html
# change the gswin64c.exe path at subproccess.popen
# python pdf_compressor.py                           / all folders
# python pdf_compressor.py start_folder end_folder   / folders in range
from __future__ import print_function
import os
import subprocess
import time
import sys
import signal
from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

main_dir = "..."

hasArgv = False
if len(sys.argv) > 2:
    start_folder = sys.argv[1]  # start folder number
    end_folder = sys.argv[2]  # end folder number
    hasArgv = True
else:
    start_folder = ""
    end_folder = ""


last_folder = ""  # last folder
last_file = ""  # compressed last file

t_start_time = time.time()
file_size_kb = 0
compressed_file_size_kb = 0
count = 0


def handler(signum, frame):  # handle terminate
    print("------------------------------------------")
    print("Sıkıştırma yapılan son")
    print("Klasör: ", last_folder)
    print("Dosya: ", last_file)

    create_log(1)

    sys.exit("Sıkıştırma durduruldu.")


signal.signal(signal.SIGINT, handler)  # crtl + c  ==> call handler

errorList = []


def create_log(p=0):  # create log
    log = open("compress-logs-inprogress.txt", "w")
    log.write("date: %s \n" % date)
    log.write("main_dir: %s \n" % main_dir)
    log.write("start_folder: %s \n" % start_folder)
    log.write("end_folder: %s \n" % end_folder)
    log.write("last_compress_folder: %s \n" % last_folder)
    log.write("last_compressed_file: %s \n" % last_file)

    if p == 1:
        log.write("subprocess terminated \n")

        if len(errorList) > 0:
            for error in errorList:
                log.write("------------------------------------------\n")
                log.write("file: %s \n" % error.file)
                log.write("error: %s \n" % error.error)
                log.write("------------------------------------------\n")

        log.close()
        os.rename("compress-logs-inprogress.txt", "%s.txt" % date)

    if p == 2:
        log.write("files: %s  \n" % count)
        log.write("total file size: %s mb \n" % file_size_mb)
        log.write("compressed file size: %s mb \n" % compressed_file_size_mb)
        log.write("compress percentage: %s \n" % compress_perc)

        if len(errorList) > 0:
            for error in errorList:
                log.write("------------------------------------------\n")
                log.write("folder: %s \n" % error[0])
                log.write("file: %s \n" % error[1])
                log.write("error: %s \n" % error[2])
                log.write("------------------------------------------\n")

        log.close()
        os.rename("compress-logs-inprogress.txt", "%s.txt" % date)


for root, dirs, files in os.walk(main_dir):
    for file in files:
        if file.endswith(".pdf"):
            filename = os.path.join(root, file)
            folder = os.path.basename(os.path.dirname(filename))

            if hasArgv:
                if int(folder) < int(start_folder) or int(folder) > int(end_folder):
                    break

            last_folder = folder

            print("Klasör: %s" % folder)
            print("%s sıkıştırılıyor..." % file)
            start_time = time.time()

            arg1 = '-sOutputFile=' + "compressed_" + file
            p = subprocess.Popen(['C:/Program Files/gs/gs9.55.0/bin/gswin64c.exe', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                                 '-dPDFSETTINGS=/ebook',  '-dNOPAUSE', '-dBATCH', '-dQUIET', str(arg1), filename], cwd=root, stdout=subprocess.PIPE)

            if p.communicate()[1] != None:
                errorList.append([folder, file, p.communicate()[1]])

            count += 1
            compressed_file_path = os.path.join(root, "compressed_" + file)
            compressed_file_size_kb += os.path.getsize(compressed_file_path)
            file_size_kb += os.path.getsize(filename)

            os.remove(filename)
            os.rename(compressed_file_path, filename)

            last_file = file

            create_log()

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

create_log(2)
