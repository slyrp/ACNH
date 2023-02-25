# Info on Hex Codes

In .pbc files, hex codes such as 16 are present. [pbc.py](https://github.com/slyrp/ACNH/blob/main/pbc.py) turns these into images with hex codes that use the 16 and turn it into #161616. These are just hex codes I've gathered through exploring.
<br>
(If you're wondering what code does this it's:


```
pix[x*2,y*2] = (a,a,a,255)
pix[x*2,y*2+1] = (b,b,b,255)
pix[x*2+1,y*2+1] = (c,c,c,255)
pix[x*2+1,y*2] = (d,d,d,255)
```

(?) = Not sure or just guessing
<br>
(-) = Pretty sure but not 100% confident
<br>
Everything else I am confident on.


16 = Walkable and/or walkway
<br>
25 = Unwalkable
<br>
17 = Carpet
<br>
06 = Wood and walkable (-)
<br>
07 = Unwalkable and unviewable by camera (?)
<br>
12 = Glass/tile (-)
<br>
36 = This is in the museum where the fishes are (?)
<br>
02 = This is in the museum where the insects are (?)
<br>
04 = This is in the museum where tanks of fish are (?)
<br>
