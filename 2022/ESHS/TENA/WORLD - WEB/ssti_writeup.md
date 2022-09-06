# World

Vamos a la URL indicada y nos pide encontrar el secreto

![picture 1](../../images/802ae6147ad827309003a45b52f8e45a3aac19f8f11e1e15ad15dc144ea62223.png)  

Entonces vamos a /secret?secret=pepe

![picture 2](../../images/f653b0e4707f048652773d943edef9be4ac3ff462f57ada2b8985d88f62f48b0.png)  

Y como vemos se esconde nuestro secreto...

Pero, si mandamos muchos caracteres, nos va a devolver un error. Y ese error nos da el codigo que encodea.

![picture 3](../../images/f35204c9aa4512fae5c208dcdfd24be37b616568e244723557aa866f336731ab.png)  

Como se puede ver, se utiliza el encoding en RC4 con la frase "HereIsTreasure". Como nota, si aplicamos RC4 a una string, y luego volvemos a aplicar RC4 a la misma string, obtenemos el string original. Vamos a provecharnos de esto.

Como se ve, la pagina hace render_template_string(safe(deS)), asi que podemos injectar algo encodeado con RC4.

Buscando encontre un script de Python que hace el Encode en RC4, y de ahi lo modificamos para que haga `str(base64.b64decode(enc_base64),'utf-8')` ya que el script tambien encodeaba a base64. <br>
Al probarlo me devolvio la siguiente URL que imprime en pantalla el texto directamente. A partir de ahora, toda injeccion ira encryptada en RC4. 

![picture 6](../../images/e7738fbf5cdfc77e6e2d79db0312620f45f3d9cca8d474daac8d1ec48f37ecf4.png)  

Ahi fue cuando pensamos que no ibamos a poder ejecutar nada, pero volviendo a un CTF que habiamos resuelto anteriormente, utilizamos 
`{{''.__class__.__mro__[1].__subclasses__()}}` lo que devuelve:

![picture 7](../../images/ff27e3c504940fd002404ebfe70ea143932bb5821b338effd9da8dcb1a2e52f6.png)  

Entonces, esto es un Server Side Template Injection.
Lo cual, con un poco de ayuda de google encontramos que podemos ir a 
`{{''.__class__.__mro__[2].__subclasses__()}}` 

![picture 8](../../images/488046e4838b60cce2f020012cf942429a7a59fbd7e4fd80038ac45b8be84011.png)  

Si bien esta clase no tiene fopen, si tiene una clase llamada `<class 'warnings.catch_warnings'>` la cual vamos a aprovechar.

![picture 9](../../images/2b6aec2e6d36aa59b128d92e8b4df55042fff7195d18b1847e99e441f92e29c6.png)  

Mediante esta clase, importamos 'os' y con esto popen para abrir el archivo flag.txt

`{{''.__class__.__mro__[2].__subclasses__()[59].__init__.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read()}}`

![picture 10](../../images/1d2aada6fe85bd1affd5fd9ddbf364e88d15a9acbba3f72916f456d7b312d2b6.png)  

```
- FLAG
T3N4CI0US{8485_c8df169b508b_f_699a4e746e_30923d4_bdd60b1a096b43a8_6_c7535ae642c3} 
```