import os
import sarc
import struct
import zstandard
from PIL import Image
from colorama import Fore, Style, init
import random
import base64
import json

# storing random stuff for when it runs
try:
    init()
except Exception as e:
    input("There was an error while initializing command prompt colors. Error: " + str(e))
try:
    cd = os.getcwd()
    da = ""
except Exception as e:
    input("There was an error while getting the current directory. Error: " + str(e))
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
    input("Error while initializing good/bad dictionary. Error: " + str(e))
try:
    if not os.path.exists(cd + "/config.json"):
        cf = input(em + 'Looks like the "cd/config.json" directory does not exist. Would you like to create it? (y/n): ')
        if cf == "y":
            with open("config.json", "w") as w:
                w.write("""
{
    "pbc": "imgs/",
    "imgs": "imgs/"
}
                        """)

            print(Fore.GREEN + gm + "Directory created successfully." + Style.RESET_ALL)
            ce = True
        else:
            input(em + "Directory not created.")
            exit()
    else:
        ce = True
except Exception as e:
    input('Error while checking for "cd/pbc" directory. Error: ' + str(e))

with open("config.json", "r+") as rc:
    try:
        config = json.load(rc)
        pbcp = config["pbc"]
        pbcpaths = pbcp.split(", ")  # split the string into separate paths

        pbcpaths = [pbc + "/" if not pbc.endswith("/") else pbc for pbc in pbcpaths]
    except ValueError:
        if "\\" in pbcp:
            print(f"{Fore.YELLOW} Backslashes cannot be used in paths, replace them with forwardslashes {Style.RESET_ALL}")
        input("cd value incorrect in config.json. Please make sure it is seperated with commas and shows correct paths. ")
        exit()

    try:
        imgsp = config["imgs"]
        imgspaths = imgsp.split(", ")  # split the string into separate paths

        imgspaths = [imgs + "/" if not imgs.endswith("/") else imgs for imgs in imgspaths]
        print(imgsp)
        print(pbcp)
    except ValueError:
        input("imgs value incorrect in config.json. Please make sure it is seperated with commas and shows correct paths. ")
        exit()


# telling the user stuff, happens on every run
print(Fore.CYAN + base64.b64decode(b'TWFkZSBieSBzbHlycCAoaHR0cHM6Ly9naXRodWIuY29tL3NseXJwL0FDTkgpICYgaGFsZi1zdG9sZW4gZnJvbSBUcmVla2kgKGh0dHBzOi8vZ2l0aHViLmNvbS9UcmVla2kvQ3lsaW5kcmljYWxFYXJ0aCk=').decode('utf-8') + Style.RESET_ALL)
print(f"Note: any .pbc or .zs files should be stored in the paths in the config for it to work!{Fore.YELLOW} YOU MUST INCLUDE THE FULL PATH! {Style.RESET_ALL}")
print("Current directory is: " + cd + '. If this is wrong open it by double-clicking instead of using "Open With."')
if ce == True:
    print(Fore.GREEN + gm + '"config.json" directory already exists.' + Style.RESET_ALL)
try:
    for pbcp in pbcpaths:
        if not os.path.exists(pbcp):
            cf = input(em + f'Looks like the "{pbcp}" directory does not exist. Would you like to create it? (y/n): ')
            if cf == "y":
                os.mkdir(pbcp)
                print(Fore.GREEN + gm + "Directory created successfully." + Style.RESET_ALL)
            else:
                input(em + "Directory not created.")
                exit()
        else:
            print(Fore.GREEN + gm + f'"{pbcp}" directory already exists.' + Style.RESET_ALL)
except Exception as e:
    input(+ f'Error while checking for "{pbcp}" directory. Error: ' + str(e))

try:
    for imgsp in imgspaths:
        if not os.path.exists(imgsp):
            cf = input(em + f"Looks like the '{imgsp}' directory does not exist. Would you like to create it? (y/n): ")
            if cf == "y":
                os.mkdir(imgsp)
                print(Fore.GREEN + gm + "Directory created successfully" + Style.RESET_ALL)
            else:
                input(em + "Directory not created")
                exit()
        else:
            print(Fore.GREEN + f"Good, '{imgsp}' directory already exists" + Style.RESET_ALL)
except Exception as e:
    input(f'Error while checking for "{imgsp}" directory. Error: ' + str(e))


#starts off by asking for file name
name = input("Please enter file name (.zs/.pbc): ")

#creating image takes like 80% of the code so i made it its own function
def createimage(name, blob, w, h, da):
    ci = input("Would you like to create an image? (y/n): ")
    if ci == "y":
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
            for eyes in imgspaths:
                try:
                    img.save(f"{eyes}/{name}.png")
                    print(Fore.GREEN + f"Saving image to: {eyes}/{name}.png" + Style.RESET_ALL)
                    print(Fore.GREEN + gm + "The file was saved successfully." + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + em + "There was a problem saving the image. Error: " + str(e) + ". Let's try that again." + Style.RESET_ALL)
                    name = input("Please enter file name (.zs/.pbc): ")
                    checkname(name)
            for s in sets:
                print(s)
                print(min(s), max(s))
        except Exception as e:
            print(Fore.RED + em + "The image couldn't be created. Error: " + str(e) + ". Let's try that again." + Style.RESET_ALL)
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
            da = input("Would you like to decompress another .zs/.pbc? (y/n): ")
            if da == "y":
                name = input("Please enter file name (.zs/.pbc): ")
            checkname(name)
        except Exception as e:
            print(Fore.RED + "Error while initializing code to decompress another file. Error: " + e + ". Let's try that again" + Style.RESET_ALL)
            name = input("Please enter file name (.zs/.pbc): ")
            checkname(name)
    else:
        exit()

# for zs files
def zs(name):
    for pbcp in pbcpaths:
        try:
            blob = open(pbcp + name, 'rb').read()
            break  # Exit the loop if the file is found
        except FileNotFoundError:
            pass  # Try the next path if the file is not found
    else:
        print(Fore.RED + em + "That file doesn't exist. Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        checkname(name)
    try:
        blob = zstandard.ZstdDecompressor().decompress(blob)
        arc = sarc.SARC(blob)
        for name in arc.list_files():
            blob = arc.get_file_data(name)
            assert(blob[0:4] == b'pbc\0')
            w, h, offset_x, offset_y = struct.unpack_from('<iiii', blob, 4)
            data = bytearray(w * h * 4)
            offset = 0x14
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
        exit()



# for pbc files
def pbc(name):
    for pbcp in pbcpaths:
        try:
            blob = open(pbcp + name, 'rb').read()
            break  # Exit the loop if the file is found
        except FileNotFoundError:
            pass  # Try the next path if the file is not found
    else:
        print(Fore.RED + em + "That file doesn't exist. Let's try that again." + Style.RESET_ALL)
        name = input("Please enter file name (.zs/.pbc): ")
        pbc(name)
    try:
        assert(blob[0:4] == b'pbc\0')
        w, h, offset_x, offset_y = struct.unpack_from('<iiii', blob, 4)
        data = bytearray(w * h * 4)
        offset = 0x14
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
