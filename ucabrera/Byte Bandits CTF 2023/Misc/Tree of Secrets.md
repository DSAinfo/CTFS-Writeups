## Tree of Secrets

The message is encoded in the whispers of the wind, buried deep in the roots of a tree. Uncover the secret by listening to the silence between the lines and exploring the branches.

Adjuntos:

[message](../attachments/message)

[root.zip](../attachments/root.zip) 

El contenido de message es:

00011000110011110000000100110000101011001111100000111101011010101101000010111100110100101001101001010001101111111111111111010111010001001

El contenido de root, una vez extraido, es: 
```bash
$ tree .
.
├── 0
│   ├── 0
│   │   ├── 0
│   │   │   └── R
│   │   └── 1
│   │       ├── 0
│   │       │   └── 3
│   │       └── 1
│   │           └── U
│   └── 1
│       ├── 0
│       │   ├── 0
│       │   │   ├── 0
│       │   │   │   └── m
│       │   │   └── 1
│       │   │       └── Z
│       │   └── 1
│       │       └── d
│       └── 1
│           ├── 0
│           │   ├── 0
│           │   │   └── t
│           │   └── 1
│           │       └── z
│           └── 1
│               ├── 0
│               │   └── i
│               └── 1
│                   └── G
└── 1
    ├── 0
    │   ├── 0
    │   │   ├── 0
    │   │   │   └── F
    │   │   └── 1
    │   │       └── 9
    │   └── 1
    │       ├── 0
    │       │   └── I
    │       └── 1
    │           ├── 0
    │           │   └── S
    │           └── 1
    │               └── V
    └── 1
        ├── 0
        │   ├── 0
        │   │   ├── 0
        │   │   │   └── k
        │   │   └── 1
        │   │       └── x
        │   └── 1
        │       └── X
        └── 1
            ├── 0
            │   ├── 0
            │   │   └── B
            │   └── 1
            │       └── T
            └── 1
                └── 0
```
Vamos a asumir que el contenido de message, se tiene que partir en partes, que permitan llegar a una hoja quedando así:
```
000 R
11000 k
11001 x
11100 B
000 R
0010 3
01100 t
0010 3
10110 S
01111 G
1000 F
0011 U
1101 X
01101 z
0101 d
1010 I
000 R
10111 V
1001 9
1010 I
0101 d
0011 U
01001 Z
01000 m
1101 X
1111 0
1111 0
1111 0
11101 T
01110 i
1000 F
1001 9
```
Lo cual forma: RkxBR3t3SGFGdISFV9IdUZmx000TiF9, probamos [cybercheff](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=Umt4QlIzdDNTR0ZVWHpkSVJWOUlkVVptWDAwMFRpRjk) y obtenemos la flag: FLAG{wHaT_7HE_HuFf_M4N!}, vamos a obtener un incorrect, despues de verificar varias veces que no hay un error de nuestra parte, recordamos que las flags van entre flag{}

Flag: flag{wHaT_7HE_HuFf_M4N!}