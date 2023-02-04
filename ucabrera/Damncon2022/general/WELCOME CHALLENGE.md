# Challenge Name : WELCOME CHALLENGE

- Challenge owner : DAMNCON2022
- Release date : 0000-00-00 00:00:00
- Dificuilty : EASY
- Points : 10
- Resource : [Click to view resources](https://dsph.org/?id=DAMNCON%252525252525257BWELCOM_2022%252525252525257D)
- Description : Decode the get object

---

Si abrimos el enlace https://dsph.org/ hay una página bastante completa, si leemos el fuente, tambien es muy completo, pero no tiene nada útil; solo tenemos que observar la URL que se abrió: https://dsph.org/?id=DAMNCON%252525252525257BWELCOM_2022%252525252525257D

Ahi podemos ver que lo que tenemos que decodificar es: DAMNCON%252525252525257BWELCOM_2022%252525252525257D, hay que descartar los %, los 25 que en hexa representan al % y pasar de hexa a ascii 7B = { y 7D = } y se obtiene la flag.

Flag: DAMNCON{WELCOM_2022}