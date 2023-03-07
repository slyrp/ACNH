# pbc.py

## pbc.py is a simple way to read and generate images for `.pbc` files.

### Code

`name = input("Please enter file name (.zs/.pbc): ")` starts off the file with asking the user for the file. `checkname()` then runs which checks if the file ends with `.zs` or `.pbc`. If the file does not end with either of these the function returns an error message and prompts the user to enter the name again.

`pbc()` and `zs()` are both mostly the same, except for the first part. `zs()` uses `blob = zstandard.ZstdDecompressor().decompress(blob)` to decompress the `.zs` file using the zstandard module. `arc = sarc.SARC(blob)` decompresses the decompressed `.zs` SARC archive. `zs()` also runs the code `for name in arc.list_files():` which simply runs the following code for all `.pbc` files in that decompressed archive.

They both then run the code:

```
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
```

First, `blob = arc.get_file_data(name)` gets the file data from the blob, it the checks the magic of the file (`pbc\0`) to make sure it's a valid `.pbc` file. It then extracts the `width`, `height`, `offset X` and `offset Y` by a `4` character offset after the magic (`<iiii`). It then uses Pythons built in `bytearray()` to get the btyearray of the file and set the `offset` to `0x14` (20 in decimal). After, it simply prints the gathered material and runs `createimage()`.

In `createimage()` it queries the user to whether they want to create an image. If the user responds "`y`," the code continues. First, it creates an empty list of twelve sets, then, it creates an image with `w*2` and `h*2`. It loads the image in a variable called `pix` (pixel) and sets the `offset` to `0x14` (20 in decimal). It scans the `width` and `height` and the `for i in range(12):` is just for logging the sets in the console. The following code represent the RGBA values for a single pixel within the new image:

```
a = blob[offset + 0x30]
b = blob[offset + 0x31]
c = blob[offset + 0x32]
d = blob[offset + 0x33]
```

The following code selects the appropriate byte values from the blob object and assigns them to variables `a`, `b`, `c`, and `d`:

```
pix[x*2,y*2] = (a,a,a,255)
pix[x*2,y*2+1] = (b,b,b,255)
pix[x*2+1,y*2+1] = (c,c,c,255)
pix[x*2+1,y*2] = (d,d,d,255)
```

These lines assign the RGBA values to corresponding pixels in the newly created image. The `pix` variable represents a `PixelAccess` object, which can be used to get or set the RGBA value for any given pixel within the image. The pixel coordinates are obtained by multiplying the loop variable `x` by 2 for the x component and `y` by 2 for the y component, then adding 1 to either the x or y coordinate as needed depending on the position we want in relation to neighboring pixels. Immediately after it sets the offset to `+ 0x34` (52 in decimal); a better way to visualize this is `offset = offset + 0x34`. `0x34` is exactly enough to access the pixel data after that pixel.
