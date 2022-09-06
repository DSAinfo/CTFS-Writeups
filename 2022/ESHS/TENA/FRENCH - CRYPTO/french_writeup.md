# French Cypher

Si buscamos cuales Cypher son de origen frances, nos encontramos con **Vigenere**

Pero si queremos hacer el Decode, nos pide una clave

![picture 11](../../images/47fa3f161d667f9a6b73e1354a997e16391131d747110d5f083b8e28ee876ca5.png)  

Al no saber cual es el tamaño de la clave, no voy a gastar tiempo intentando bruteforcearla. Si se que la clave es solo alfabetica. <br>
No obstante, el CTF solo ofrece el valor 'V3Y4GK0FW{EccrEsXpvtjIcdc}' y la pista de que es un Cypher Frances.

Luego de intentar varias claves aleatorias (para ver si con un poco de suerte nos salia la flag), fui a otros retos. Unos de ellos tenia

![picture 12](../../images/3da788673f45a5b0317bff30c01c3357bce5d8f294dafac8a400a7e200425878.png)  

Al hacer la prueba con esa clave, obtuve la flag

![picture 13](../../images/8d0dbef5bd0e5ba58092919873840df54e2ce05df1bf69e6bd9bd98fd5bbc648.png)  

```
Flag: T3N4CI0US{CrypToVerryEasy}
```