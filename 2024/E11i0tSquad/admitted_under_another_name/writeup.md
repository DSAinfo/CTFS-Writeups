# Admitted Under Another Name

Reto de la categoría **Database / SQL** del DEADFACE CTF (creado por @syyntax). El enunciado cuenta que DEADFACE se robó el registro de pacientes de Aurora Health y que ahí adentro hay un paciente de alto perfil que se internó con un nombre falso, al que el personal marcó "en silencio" como VIP. Hay que entrar a la base, encontrarlo y reportar su MRN (Medical Record Number) real.

La flag se entrega como `deadface{MRN}` (ejemplo: `deadface{AH-1234567}`).

## Entrando a la base

El botón "Access Database" abre una terminal web (ttyd) que ya nos deja adentro de un cliente MySQL, conectados como usuario `player`. Un detalle que nos llamó la atención: el enunciado habla de "MSSQL", pero cuando se abre la terminal el banner es de MySQL/MariaDB (MySQL 8.0.46), así que terminamos resolviendo todo con sintaxis de MySQL.

Como no conocíamos nada de la base, fuimos enumerando de lo más general a lo más específico. Primero, qué bases hay:

```sql
SHOW DATABASES;
```
```
aurora_audit
aurora_ehr
aurora_pharmacy
aurora_trials
information_schema
performance_schema
```

Entramos y listamos las tablas buscando en ellas la de `patients` y la econtramos en aurora_ehr:

```sql
USE aurora_ehr;
SHOW TABLES;
```
```
clinical_notes
diagnoses
encounters
insurance_plans
patients
providers
```

Miramos cómo estaba armada:

```sql
DESCRIBE patients;
```

De todas las columnas nos quedamos con tres: `mrn` (el número que hay que reportar), `alias` (el nombre falso) y, sobre todo, `is_vip`, un campo tipo booleano (0/1).

## Sacando al VIP

Con eso ya fue directo. Filtramos por `is_vip = 1`

```sql
SELECT mrn, first_name, last_name, alias, is_vip, deleted_at
FROM patients
WHERE is_vip = 1
```
```
        mrn: AH-0044719
 first_name: Gregory
  last_name: Halloran
      alias: George Harmon
     is_vip: 1
 deleted_at: NULL
```

Nos devolvió una sola fila, así que no había ninguna ambigüedad: el paciente VIP es Gregory Halloran, internado como "George Harmon". Metimos también `deleted_at` por las dudas de que el registro estuviera oculto con un *soft delete*, pero estaba en `NULL`.

El MRN real es `AH-0044719`, así que la flag quedó:

```
deadface{AH-0044719}
```

El script [`solve.py`](./solve.py) automatiza la consulta final.
