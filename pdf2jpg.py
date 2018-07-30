from subprocess import check_call
from os.path import splitext, basename
from os import unlink, listdir
from zipfile import ZipFile
from os import makedirs, rmdir


def convert2pdf(pdf, publication, ts):
    publication_ts = str(publication) + ts
    working_dir = '/Novus_flask/uploaded/{}'.format(publication_ts)
    makedirs('/Novus_flask/zip/{}'.format(publication_ts))
    jpg = splitext(pdf)[0] + ".jpg"
    check_call(["convert", "-quality", "100%", "-density", "300", pdf, jpg])
    unlink(pdf)

    with ZipFile('zip/{}.zip'.format(publication_ts), mode='a') as zf:
        for pic in listdir(working_dir):
            zf.write(working_dir + '/' + pic, basename(pic))
            unlink(working_dir + '/' + pic)
    rmdir(working_dir)
    unlink(jpg)

