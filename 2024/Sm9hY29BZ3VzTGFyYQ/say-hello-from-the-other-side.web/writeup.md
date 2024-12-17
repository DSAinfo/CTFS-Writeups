El reto consistía en interactuar con un servidor web en la URL http://159.223.126.39:9995/ que esperaba un saludo específico en el encabezado User-Agent. La respuesta del servidor era "Wrong" cuando el saludo era incorrecto. El objetivo era encontrar el "User-Agent" correcto que generaría una respuesta válida.

El primer enfoque fue realizar un ataque de fuerza bruta utilizando un script en Bash que probaba una serie de user-agents comunes. Al ejecutar el script con una lista genérica de agentes, no obtuvimos ninguna respuesta válida, siempre recibía la respuesta "Wrong". Ante este resultado, decidimos releer el título del reto: "Say Hello From the Other Side", dandonos cuenta de que la frase "Other Side" parecía ser una pista clara sobre el saludo que el servidor esperaba.

Modificamos el script agregando "Other Side" al final de la lista de user-agents y volví a ejecutar la prueba. Esta vez, el servidor respondió correctamente, indicando que habíamos encontrado el saludo esperado. 

flag{W3_s4lut3_y0u_fr0m_Th3_0th3r_Sid3}