from subprocess import check_call
from os.path import splitext, basename
from os import unlink, listdir
from zipfile import ZipFile
from datetime import datetime
from multiprocessing import Pool


working_dir = '/Novus_flask/uploaded/'
original_zipfile = '/Novus_flask/zip/converted.zip'


def convert2pdf(pdf):
    jpg = splitext(pdf)[0] + ".jpg"
    with Pool(processes=20) as pool:
        pool.map(check_call(["convert", "-quality", "100%", "-density", "600", pdf, jpg]))
    unlink(pdf)
    if original_zipfile:
        unlink(original_zipfile)

    with ZipFile('/Novus_flask/zip/converted.zip', mode='a') as zf:
        for pic in listdir(working_dir):
            zf.write(working_dir + pic, basename(pic))
            unlink(working_dir + pic)
    unlink(jpg)

