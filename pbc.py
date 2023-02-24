import os
import sarc
import struct
import zstandard
from PIL import Image
from colorama import Fore, Style, init
import random
import base64

# storing random stuff for when it runs
try:
    init()
except Exception as e:
    input(Fore.RED + "There was an error while initializing command prompt colors. Error: " + str(e) + Style.RESET_ALL)
try:
    cd = os.getcwd()
    da = ""
except Exception as e:
    input(Fore.RED + "There was an error while getting the current directory. Error: " + str(e) + Style.RESET_ALL)
try:
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
except Exception as e:
    input(Fore.RED + "Error while initializing good/bad dictionary. Error: " + str(e) + Style.RESET_ALL)


# telling the user stuff, happens on every run
print(Fore.CYAN + base64.b64decode(b'TWFkZSBieSBzbHlycCAoaHR0cHM6Ly9naXRodWIuY29tL3NseXJwL0FDTkgpICYgaGFsZi1zdG9sZW4gZnJvbSBUcmVla2kgKGh0dHBzOi8vZ2l0aHViLmNvbS9UcmVla2kvQ3lsaW5kcmljYWxFYXJ0aCk=').decode('utf-8') + Style.RESET_ALL)
print("Note: any .pbc or .zs files should be stored in cd/pbc for it to work!")
print("Note: for images, light grey is unwalkable, dark grey is walkable.")
print("Current directory is: " + cd + '. If this is wrong open it by double-clicking instead of using "Open With."')
try:
    if not os.path.exists(cd + "/pbc"):
        cf = input(Fore.RED + em + 'Looks like the "cd/pbc" directory does not exist. Would you like to create it? (y/n): ' + Style.RESET_ALL)
        if cf == "y":
            os.mkdir("pbc")
            print(Fore.GREEN + gm + "Directory created successfully." + Style.RESET_ALL)
        else:
            input(Fore.RED + em + "Directory not created." + Style.RESET_ALL)
            exit()
    else:
        print(Fore.GREEN + gm + '"/pbc" directory already exists.' + Style.RESET_ALL)
except Exception as e:
    input(Fore.RED + 'Error while checking for "cd/pbc" directory. Error: ' + str(e) + Style.RESET_ALL)


#starts off by asking for file name
name = input("Please enter file name (.zs/.pbc): ")

#creating image takes like 80% of the code so i made it its own function
def createimage(name, blob, w, h, da):
    ci = input("Would you like to create an image? (y/n): ")
    if ci == "y":
        try:
            if not os.path.exists(cd + "/imgs"):
                cf = input(Fore.RED + em + "Looks like the 'cd/imgs' directory does not exist. Would you like to create it? (y/n): " + Style.RESET_ALL)
                if cf == "y":
                    os.mkdir("imgs")
                    print(Fore.GREEN + gm + "Directory created successfully" + Style.RESET_ALL)
                else:
                    print(Fore.RED + em + "Directory not created" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Good, '/imgs' directory already exists" + Style.RESET_ALL)
        except Exception as e:
            input('Error while checking for "cd/imgs" directory. Error: ' + str(e))
        try:
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
        except Exception as e:
            print(Fore.RED + em + "Your image couldn't be saved. Error: " + str(e) + ". Let's try that again." + Style.RESET_ALL)
            name = input("Please enter file name (.zs/.pbc): ")
            zs(name)
        try:
            print(Fore.GREEN + 'Saving image to:', 'imgs/%s.png' % name + Style.RESET_ALL)
            print(Fore.GREEN + gm + "The file was saved successfully." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + em + "There was a problem saving the image. Error: " + str(e) + ". Let's try that again." + Style.RESET_ALL)
            name = input("Please enter file name (.zs/.pbc): ")
            zs(name)
        da = input("Would you like to decompress another .zs/.pbc? (y/n): ")
        if da == "y":
            name = input("Please enter file name (.zs/.pbc): ")
            checkname(name)
        else:
            exit()
    elif ci == "n":
        try:
            name = input("Would you like to decompress another .zs/.pbc? (y/n): ")
            if da == "y":
                name = input("Please enter file name (.zs/.pbc): ")
            checkname(name)
        except Exception as e:
            print(Fore.RED + "Error while initializing code to decompress another file. Error: " + e)
    else:
        exit()

# for zs files
def zs(name):
    try:
        blob = open('pbc/' + name, 'rb').read()
    except:
        print(Fore.RED + em + "There was a problem opening that file, maybe the file doesn't exist? Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        zs(name)
    try:
        blob = zstandard.ZstdDecompressor().decompress(blob)
        arc = sarc.SARC(blob)
        for name in arc.list_files():
            blob = arc.get_file_data(name)
            assert(blob[0:4] == b'pbc\0')
            w, h, offset_x, offset_y = struct.unpack_from('<iiii', blob, 4)
            data = bytearray(w * h * 4)
            offset = 0x14
            for y in range(h):
                for x in range(w):
                    a, b, c, d = blob[offset+0x30:offset+0x34]
                    data[(x*2)   + ((y*2)  *(w*2))] = a
                    data[(x*2)   + ((y*2+1)*(w*2))] = b
                    data[(x*2+1) + ((y*2+1)*(w*2))] = c
                    data[(x*2+1) + ((y*2)  *(w*2))] = d
                    offset += 0x34
            print("Raw decompressed data: " + str(data))
            print(name + ": ")
            print("Width: " + str(w))
            print("Height: " + str(h))
            print("Offset X: " + str(offset_x))
            print("Offset Y: " + str(offset_y))
    except Exception as e:
        print(Fore.RED + em + "Looks like your .zs file could not be decompressed correctly. Error: " + str(e) + ". Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        zs(name)
    try:
        createimage(name, blob, w, h, da)
    except Exception as e:
        print(Fore.RED + 'Error while initiating "createimage(). Error: ' + str(e))



# for pbc files
def pbc(name):
    try:
        blob = open('pbc/' + name, 'rb').read()
    except:
        print(Fore.RED + em + "That file doesn't exist. Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        pbc(name)
    try:
        assert(blob[0:4] == b'pbc\0')
        w, h, offset_x, offset_y = struct.unpack_from('<iiii', blob, 4)
        data = bytearray(w * h * 4)
        offset = 0x14
        for y in range(h):
            for x in range(w):
                a, b, c, d = blob[offset+0x30:offset+0x34]
                data[(x*2)   + ((y*2)  *(w*2))] = a
                data[(x*2)   + ((y*2+1)*(w*2))] = b
                data[(x*2+1) + ((y*2+1)*(w*2))] = c
                data[(x*2+1) + ((y*2)  *(w*2))] = d
                offset += 0x34
        print("Raw decompressed data: " + str(data))
        print(name + ": ")
        print("Width: " + str(w))
        print("Height: " + str(h))
        print("Offset X: " + str(offset_x))
        print("Offset Y: " + str(offset_y))
    except Exception as e:
        print(Fore.RED + em + "Looks like your .zs file could not be decompressed correctly. Error: " + str(e) + ". Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        pbc(name)
    createimage(name, blob, w, h, da)

# checking if file ends with zs or pbc
def checkname(name):
    if name.endswith(".zs"):
        zs(name)
    elif name.endswith(".pbc"):
        pbc(name)
    else:
        print(Fore.RED + em + "That's not a valid file. Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        checkname(name)

# runs everything, hooray
checkname(name)
