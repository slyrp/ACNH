import os
import sarc
import struct
import zstandard
from PIL import Image
from colorama import Fore, Style, init
import random

init()
cd = os.getcwd()
emu = [
    "Uh-oh! ",
    "Oops! ",
    "Whoops! ",
    "Something went wrong! ",
    "There's been an error. ",
    "Something happened. ",
    "An error has occured! ",
    "Do you see that? Oh! "
]
em = random.choice(emu)
gmu = [
    "Woohoo! ",
    "Amazing. ",
    "Good news! ",
    "Great. ",
    "Hooray! ",
    "Success. "
]
gm = random.choice(gmu)

print("Note: any .pbc or .zs files should be stored in *folder*/pbc for it to work!")
if not os.path.exists(cd + "/pbc"):
    cf = input(Fore.RED + em + "Looks like the '*folder*/pbc' directory does not exist. Would you like to create it? (y/n) " + Style.RESET_ALL)
    if cf == "y":
        os.mkdir("pbc")
        print(Fore.GREEN + gm + "Directory created successfully" + Style.RESET_ALL)
    else:
        print(Fore.RED + em + "Directory not created"+ Style.RESET_ALL )
else:
    print(Fore.GREEN + gm + "'/pbc' directory already exists" + Style.RESET_ALL)

name = input("Please enter file name (.zs/.pbc): ")

def zs(name):
    try:
        blob = open('pbc/' + name, 'rb').read()
    except:
        print(Fore.RED + em + "That file doesn't exist. Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        zs(name)
    try:
        blob = zstandard.ZstdDecompressor().decompress(blob)
        arc = sarc.SARC(blob)

        for name in arc.list_files():
            blob = arc.get_file_data(name)
            assert(blob[0:4] == b'pbc\0')
            w,h,offset_x,offset_y = struct.unpack_from('<iiii', blob, 4)
            data = bytearray(w * h * 4)
            print("Raw decompiled data:")
            print(data)
            print("                Width Height Offset X Offset Y")
            print(name, w, "   ", h, "    ", offset_x, "     ", offset_y)
    except:
        print(Fore.RED + em + "Looks like your .zs file could not be decompressed correctly. Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        zs(name)
    ci = input("Would you like to create an image? (y/n): ")
    if ci == "y":
        try:
            if not os.path.exists(cd + "/imgs"):
                cf = input(Fore.RED + em + "Looks like the '*folder*/imgs' directory does not exist. Would you like to create it? (y/n): " + Style.RESET_ALL)
                if cf == "y":
                    os.mkdir("imgs")
                    print(Fore.GREEN + gm + "Directory created successfully" + Style.RESET_ALL)
                else:
                    print(Fore.RED + em + "Directory not created" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Good, '/pbc' directory already exists" + Style.RESET_ALL)
            sets = [set() for i in range(12)]
            img = Image.new('RGBA', (w*2, h*2))
            pix = img.load()
            offset = 0x14
            for y in range(h):
                for x in range(w):
                    for i in range(12):
                        f = struct.unpack_from('<f', blob, offset + i * 4)[0]
                        sets[i].add(f)
                    a = blob[offset + 0x30]
                    b = blob[offset + 0x31]
                    c = blob[offset + 0x32]
                    d = blob[offset + 0x33]
                    pix[x*2,y*2] = (a,a,a,255)
                    pix[x*2,y*2+1] = (b,b,b,255)
                    pix[x*2+1,y*2+1] = (c,c,c,255)
                    pix[x*2+1,y*2] = (d,d,d,255)
                    offset += 0x34
            img.save('imgs/%s.png' % name)
            for s in sets:
                print(s)
                print(min(s), max(s))
        except:
            print(Fore.RED + em + "Your image couldn't be saved for some reason. Let's try that again." + Style.RESET_ALL)
            name = input("Please enter file name (.zs/.pbc): ")
            zs(name)
        try:
            print(Fore.GREEN + 'Saving image to:', 'imgs/%s.png' % name + Style.RESET_ALL)
            print(Fore.GREEN + gm + "The file was saved successfully." + Style.RESET_ALL)
            input("Press enter to exit.")
        except:
            print(Fore.RED + em + "There was a problem saving the image. Let's try that again." + Style.RESET_ALL)
            name = input("Please enter file name (.zs/.pbc): ")
            zs(name)
    elif ci == "n":
        input("Press enter to exit.")






def pbc(name):
    try:
        blob = open('pbc/' + name, 'rb').read()
    except:
        print(Fore.RED + em + "That file doesn't exist. Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        zs(name)
    try:
        assert(blob[0:4] == b'pbc\0')
        w,h,offset_x,offset_y = struct.unpack_from('<iiii', blob, 4)
        data = bytearray(w * h * 4)
        print("Raw decompressed data:")
        print(data)
        print("                Width Height Offset X Offset Y")
        print(name, w, "   ", h, "    ", offset_x, "     ", offset_y)
    except:
        print(Fore.RED + em + "Looks like your .zs file could not be decompressed correctly. Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        zs(name)
    ci = input("Would you like to create an image? (y/n): ")
    if ci == "y":
        try:
            if not os.path.exists(cd + "/imgs"):
                cf = input(Fore.RED + em + "Looks like the '*folder*/imgs' directory does not exist. Would you like to create it? (y/n): " + Style.RESET_ALL)
                if cf == "y":
                    os.mkdir("imgs")
                    print(Fore.GREEN + gm + "Directory created successfully" + Style.RESET_ALL)
                else:
                    print(Fore.RED + em + "Directory not created" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Good, '/pbc' directory already exists" + Style.RESET_ALL)
            sets = [set() for i in range(12)]
            img = Image.new('RGBA', (w*2, h*2))
            pix = img.load()
            offset = 0x14
            for y in range(h):
                for x in range(w):
                    for i in range(12):
                        f = struct.unpack_from('<f', blob, offset + i * 4)[0]
                        sets[i].add(f)
                    a = blob[offset + 0x30]
                    b = blob[offset + 0x31]
                    c = blob[offset + 0x32]
                    d = blob[offset + 0x33]
                    pix[x*2,y*2] = (a,a,a,255)
                    pix[x*2,y*2+1] = (b,b,b,255)
                    pix[x*2+1,y*2+1] = (c,c,c,255)
                    pix[x*2+1,y*2] = (d,d,d,255)
                    offset += 0x34
            img.save('imgs/%s.png' % name)
            for s in sets:
                print(s)
                print(min(s), max(s))
        except:
            print(Fore.RED + em + "Your image couldn't be saved for some reason. Let's try that again." + Style.RESET_ALL)
            name = input("Please enter file name (.zs/.pbc): ")
            zs(name)
        try:
            print(Fore.GREEN + 'Saving image to:', 'imgs/%s.png' % name + Style.RESET_ALL)
            print(Fore.GREEN + gm + "The file was saved successfully." + Style.RESET_ALL)
            input("Press enter to exit.")
        except:
            print(Fore.RED + em + "There was a problem saving the image. Let's try that again." + Style.RESET_ALL)
            name = input("Please enter file name (.zs/.pbc): ")
            zs(name)
    elif ci == "n":
        input("Press enter to exit.")

def checkname(name):
    if name.endswith(".zs"):
        zs(name)
    elif name.endswith(".pbc"):
        pbc(name)
    else:
        print(Fore.RED + em + "That's not a valid file. Let's try again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        checkname(name)
checkname(name)
