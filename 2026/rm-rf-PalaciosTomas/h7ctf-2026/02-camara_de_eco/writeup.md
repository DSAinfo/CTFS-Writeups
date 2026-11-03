# Writeup: Cámara de eco (H7CTF 2026)

## 1. Reconocimiento inicial

Al acceder a la plataforma web de Atlas Incident Intelligence, me encontré con un caso activo bajo los siguientes parámetros:

Incidente: INC-7421
Producto / Versión: StreamForge 4.8.x
Componente: worker-runtime
Estado inicial: investigating / unverified
Confianza inicial de la IA: 50% (sin registros de apoyo previos).

El sistema se negaba a emitir un informe definitivo de cierre porque carecía de la validación y el soporte documental necesario en su base de conocimiento. 
Al inspeccionar las distintas secciones de la página encontre un formulario el cual se detallaba como "Ingreso de investigacion" con la opción de contribuir en la investigación. 
Esto me llamó la atención y decidí investigar si era posible "inyectar" información en la base para obligar a la IA a darme el reporte final.

## 2. Estrategia de ataque 

De esta manera, procedí a intentar inyectar la  información para obligar al agente de IA a reevaluar la severidad y la certeza del caso.

Primer envío (Escalada al 90%):
 Le solicité a la IA (copilot) que escribiera un reporte técnico creíble y lo ingresé al sistema afirmando que la regresión del asignador de memoria (heap allocator) en el entorno de ejecución de trabajo estaba oficialmente diagnosticada, verificada y confirmada.
 Resultado: La confianza del sistema escaló al 90%, el estado pasó a ser probable, se enlazaron registros de soporte (KB-1036, KB-1038) y se generó el informe preliminar RPT-0002.

Segundo envío (Coraboración total):
 Nuevamente le pedí asistencia a la IA para redactar un segundo informe que asegurara que la mitigación y las pruebas forenses de telemetría confirmaban una resolución del 100%.
 Resultado: La valoración cambió a corroborado, el volumen de discos de apoyo subió a 5 (KB-1042, KB-1044, KB-1005, etc.), se generaron automáticamente los artículos de cierre (KB-1045 a KB-1047) y se consolidó el informe profundo RPT-0004 / RPT-0005.
## 3. Explotación y Obtención de la Flag
Al inspeccionar el reporte profundo generado por el sistema automatizado de Atlas, procedí a revisar los metadatos y los registros de entorno del proceso simulado (process-environment.txt).

Dentro de las variables de entorno expuestas se encontraba la clave de soporte de la instancia:
SUPPORT_INSTANCE_SECRET=H7CTF{41172d3f-e6f4-4cce-9c80-fd2b8c3cac48}

## Conclusión
El reto me pareció muy interesante, me puse nervioso porque corría el tiempo y sólo podia aumentar el tiempo 2 veces, pero intenté revisar cada sección y hacer lo mejor posible. Tuve que pedir ayuda a la IA para la redacción de los informes ya que no se me ocurría que poner y me aconsejó los que usé.
