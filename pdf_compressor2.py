# download Ghostscript https://www.ghostscript.com/download.html
# change gswin64c.exe path // gswin_path
# change pdf directory // main_dir

from __future__ import print_function
import os
import subprocess
import time
import sys
import signal
from datetime import datetime
import argparse

gswin_path = 'C:/Program Files/gs/gs9.55.0/bin/gswin64c.exe'
main_dir = r"C:\Users\user\Desktop\x\python\pdf_compressor\test-data"

parser = argparse.ArgumentParser()

# compressed_file_list path
parser.add_argument("-cl", "--compressed_list",
                    required=False, type=str, help="sıkıştırılma işlemi yapılmış dosya isimlerinin bulunduğu txt dosyası")

# create compressed files list log
parser.add_argument("-lc", "--log_compressed_list",
                    required=False, type=str, default="true", help="sıkıştırılma işlemi yapılmış dosya isimlerinin bulunduğu txt dosyasını oluşturur")

# day difference dd format
parser.add_argument("-d", "--day",
                    required=False, type=int, help="sıkıştırılma işlemi yapılmayacak son gün sayısı")

args = parser.parse_args()

lines = []
if args.compressed_list != None:
    file = open(args.compressed_list, "r")
    lines = file.read().splitlines()


date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')


t_start_time = time.time()
file_size_kb = 0
compressed_file_size_kb = 0
count = 0


def handler(signum, frame):  # handle terminate
    print("------------------------------------------")
    error_log(1)
    sys.exit("Sıkıştırma durduruldu.")


signal.signal(signal.SIGINT, handler)  # crtl + c  ==> call handler

if args.log_compressed_list == "true":
    compressd_file_logs = open("compressed_file_list_%s.txt" % date, "w")


def compressed_file_list(compressed_file):
    compressd_file_logs.write("%s\n" % compressed_file)


errorList = []
log = open("error_log_%s.txt" % date, "w")
log.write("date: %s \n" % date)
log.write("main_dir: %s \n" % main_dir)


def error_log(p):  # create log
    if p == 1:
        log.write("subprocess terminated \n")
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


def check_date(filename):
    file_date = datetime.fromtimestamp(
        os.path.getmtime(filename))

    max_day_difference = args.day

    day_difference = (datetime.now() - file_date).days

    if day_difference < max_day_difference:
        return "break"


for root, dirs, files in os.walk(main_dir):
    for file in files:
        if file.endswith(".pdf"):
            filename = os.path.join(root, file)
            folder = os.path.basename(os.path.dirname(filename))

            if args.compressed_list != None:
                if file in lines:
                    break

            if args.day != None:
                if check_date(filename) == "break":
                    break

            print("Klasör: %s" % folder)
            print("%s sıkıştırılıyor..." % file)
            start_time = time.time()

            arg1 = '-sOutputFile=' + "compressed_" + file

            try:
                p = subprocess.Popen([gswin_path, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                                      '-dPDFSETTINGS=/ebook',  '-dNOPAUSE', '-dBATCH', '-dQUIET', str(arg1), filename], cwd=root, stdout=subprocess.PIPE)

                p.communicate()

                count += 1
                compressed_file_path = os.path.join(root, "compressed_" + file)
                compressed_file_size_kb += os.path.getsize(
                    compressed_file_path)
                file_size_kb += os.path.getsize(filename)

                os.remove(filename)
                os.rename(compressed_file_path, filename)

                if args.log_compressed_list == "true":
                    compressed_file_list(filename)
            except:
                errorList.append([folder, file, sys.exc_info()[0]])
                print("Error Occured")

            print("işlem süresi:  %s saniye " %
                  ("{:.2f}".format(time.time() - start_time)))
            print("------------------------------------------")

print("Toplam işlem süresi:  %s saniye " %
      ("{:.2f}".format(time.time() - t_start_time)))

file_size_mb = "{:.2f}".format(file_size_kb / (1024*1024))
compressed_file_size_mb = "{:.2f}".format(
    compressed_file_size_kb / (1024*1024))

try:
    compress_perc = "{:.2f}".format(
        ((file_size_kb - compressed_file_size_kb) / file_size_kb) * 100)
except:
    compress_perc = "-"

print("Sıkıştırılan dosya: %s adet" % count)
print("Toplam boyut: %s mb" % file_size_mb)
print("Sıkıştırılmış toplam boyut: %s mb" % compressed_file_size_mb)
print("Sıkıştırma oranı: %s" % compress_perc)

error_log(2)
