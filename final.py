#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sys, os, re
from fake_useragent import UserAgent


def head_url():
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    return headers


def clean():
    print("cleaning old files")
    if os.path.exists(apk):
        os.remove(apk)


def grab(req, apk, link):
    with open(apk, "wb") as f:
        print("Downloading %s" % apk)
        response = req.get(link, stream=True, headers=head_url())
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()

def fileopen(versi, MD5):
    loc = "yowsup/env/env_android.py"
    locbak = "yowsup/env/env_android.py_bak"

    print("Cleaning old backup")
    if os.path.exists(locbak):
        os.remove(locbak)

    print("Making new backup")
    from shutil import copyfile
    copyfile(loc, locbak)

    fmd5 = '_MD5_CLASSES = "' + MD5 + '"'
    fversi = ' _VERSION = "' + versi + '"'

    print("Writing new settings")
    f=open(loc, "w+")
    for line in open(locbak,'r').readlines():
        tmp1 = re.sub(r' _VERSION =.+',fversi, line)
        tmp1 = re.sub(r'_MD5_CLASSES =.+',fmd5, tmp1)
        f.write(tmp1)
    f.close()

def dexmd5():
    from pyaxmlparser import APK
    import base64
    import zipfile
    import hashlib
    print("Running dexmd5")
    try:
        zipFile = zipfile.ZipFile(apk, 'r')
        classesDexFile = zipFile.read('classes.dex')
        hash = hashlib.md5()
        hash.update(classesDexFile)
        versi = APK(apk).version_name
        MD5 = base64.b64encode(hash.digest()).decode("utf-8")
    except: pass
    return versi, MD5


def download():
    print("Finding link")
    req = requests.Session()
    try:
        page = req.get("https://www.whatsapp.com/android/", headers=head_url())
    except:
        print(gloOp.error + tint("r", " Please check link is valid"))

    soup = BeautifulSoup(page.content, 'html.parser')
    for a in soup.find_all('a', href=True):
        if apk in a['href']:
            link = a['href']
    if not 'link' in locals():
        print("ERROR: Link not found")
        exit()

    print("Link found!")
    r = req.get(link, allow_redirects=True, headers=head_url())
    open(apk, 'wb').write(r.content)

    grab(req, apk, link)

    versi, MD5 = dexmd5()

    print(versi)
    print(MD5)

    fileopen(versi, MD5)


apk = "WhatsApp.apk"
clean()
download()
print("Complete")