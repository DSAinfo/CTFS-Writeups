// Correr con node -> node solve.js

function decryptXOR(inpString, xorKey) {
    inpString = inpString.split("");
 
    // para cada carácter del string, se hace el XOR con la key
    for (let i = 0; i < inpString.length; i++)
    {
        inpString[i] = (String.fromCharCode((inpString[i].charCodeAt(0)) ^ xorKey.charCodeAt(0)));
    }
    return inpString.join("");
}

const fs = require('fs');

fs.readFile('megaxord.txt', 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    const decrypted = decryptXOR(data, 'X');
    
    //buscamos el flag en el texto desencriptado
    const index = decrypted.indexOf("buckeye{");
    if (index > -1) {
        console.log("Flag: " + decrypted.substring(index, decrypted.indexOf("}", index) + 1));
    }
  });
  