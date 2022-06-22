function hexToText(hex) {
    let text = "";
    let i = 0;
    while (i < hex.length) {
        let code = 0;
        let j = 0;
        while (j < 2) {
            switch (hex[i + j]) {
                case "0":
                    code += 0;
                    break;
                case "1":
                    code += 16 ** j;
                    break;
                case "2":
                    code += 2 * (16 ** j);
                    break;
                case "3":
                    code += 3 * (16 ** j);
                    break;
                case "4":
                    code += 4 * (16 ** j);
                    break;
                case "5":
                    code += 5 * (16 ** j);
                    break;
                case "6":
                    code += 6 * (16 ** j);
                    break;
                case "7":
                    code += 7 * (16 ** j);
                    break;
                case "8":
                    code += 8 * (16 ** j);
                    break;
                case "9":
                    code += 9 * (16 ** j);
                    break;
                case "a":
                    code += 10 * (16 ** j);
                    break;
                case "b":
                    code += 11 * (16 ** j);
                    break;
                case "c":
                    code += 12 * (16 ** j);
                    break;
                case "d":
                    code += 13 * (16 ** j);
                    break;
                case "e":
                    code += 14 * (16 ** j);
                    break;
                case "f":
                    code += 15 * (16 ** j);
                    break;
            }
            j++;
        }
        text += String.fromCharCode(code);
        i += 2;
    }
    return text;
}

function textToHex(text) {
    let hex = "";
    let i = 0;
    while (i < text.length) {
        let ch = "";
        switch ((text[i].charCodeAt(0)) % 16) {
            case 0:
                ch += "0"
                break;
            case 1:
                ch += "1"
                break;
            case 2:
                ch += "2"
                break;
            case 3:
                ch += "3"
                break;
            case 4:
                ch += "4"
                break;
            case 5:
                ch += "5"
                break;
            case 6:
                ch += "6"
                break;
            case 7:
                ch += "7"
                break;
            case 8:
                ch += "8"
                break;
            case 9:
                ch += "9"
                break;
            case 10:
                ch += "a"
                break;
            case 11:
                ch += "b"
                break;
            case 12:
                ch += "c"
                break;
            case 13:
                ch += "d"
                break;
            case 14:
                ch += "e"
                break;
            case 15:
                ch += "f"
                break;
        }
        switch (Math.floor(text[i].charCodeAt(0) / 16)) {
            case 0:
                ch += "0"
                break;
            case 1:
                ch += "1"
                break;
            case 2:
                ch += "2"
                break;
            case 3:
                ch += "3"
                break;
            case 4:
                ch += "4"
                break;
            case 5:
                ch += "5"
                break;
            case 6:
                ch += "6"
                break;
            case 7:
                ch += "7"
                break;
            case 8:
                ch += "8"
                break;
            case 9:
                ch += "9"
                break;
            case 10:
                ch += "a"
                break;
            case 11:
                ch += "b"
                break;
            case 12:
                ch += "c"
                break;
            case 13:
                ch += "d"
                break;
            case 14:
                ch += "e"
                break;
            case 15:
                ch += "f"
                break;
        }
        hex += ch;
        i++;
    }
    return hex;
}

function getRandomInt() {
    let cryptoStor = new Uint16Array(20);
    let rand = (window.crypto.getRandomValues(cryptoStor)[0].toString() +
        window.crypto.getRandomValues(cryptoStor)[1].toString() +
        window.crypto.getRandomValues(cryptoStor)[2].toString() +
        window.crypto.getRandomValues(cryptoStor)[3].toString() +
        window.crypto.getRandomValues(cryptoStor)[4].toString() +
        window.crypto.getRandomValues(cryptoStor)[5].toString() +
        window.crypto.getRandomValues(cryptoStor)[6].toString() +
        window.crypto.getRandomValues(cryptoStor)[7].toString() +
        window.crypto.getRandomValues(cryptoStor)[8].toString() +
        window.crypto.getRandomValues(cryptoStor)[9].toString() +
        window.crypto.getRandomValues(cryptoStor)[10].toString() +
        window.crypto.getRandomValues(cryptoStor)[11].toString() +
        window.crypto.getRandomValues(cryptoStor)[12].toString() +
        window.crypto.getRandomValues(cryptoStor)[13].toString() +
        window.crypto.getRandomValues(cryptoStor)[14].toString() +
        window.crypto.getRandomValues(cryptoStor)[15].toString() +
        window.crypto.getRandomValues(cryptoStor)[16].toString() +
        window.crypto.getRandomValues(cryptoStor)[17].toString() +
        window.crypto.getRandomValues(cryptoStor)[18].toString() +
        window.crypto.getRandomValues(cryptoStor)[19].toString()).slice(0, 20);
    return "0." + rand;
}

function get_password_length() {
    let cryptoStor = new Uint16Array(2);
    let rand = Number((window.crypto.getRandomValues(cryptoStor)[0].toString() +
        window.crypto.getRandomValues(cryptoStor)[1].toString()).slice(0, 2));
    if (rand < 25) {
        return 19;
    }
    if (rand < 50) {
        return 20;
    }
    if (rand < 75) {
        return 21;
    } else {
        return 22;
    }
}

function generate_randomness(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Number(getRandomInt()) *
            charactersLength));
    }
    return result;
}

function generate_counter() {
    return getRandomInt().slice(2, 18);
}

function encrypt(text) {
    const textBytes = aesjs.utils.utf8.toBytes(text);
    let password = generate_randomness(get_password_length());
    let counter = generate_counter();
    const pwd = new buffer.SlowBuffer(password.slice(4, password.length).normalize('NFKC'));
    const salt = new buffer.SlowBuffer(password.slice(0, 4).normalize('NFKC'));
    const key = scrypt.syncScrypt(pwd, salt, 8, 256 / 8, 1, 32);
    const aesCtr = new aesjs.ModeOfOperation.ctr(key, new aesjs.Counter(Number(counter)));
    const encryptedBytes = aesCtr.encrypt(textBytes);
    const encryptedHex = aesjs.utils.hex.fromBytes(encryptedBytes);
    const encryptedText = hexToText(encryptedHex);
    return Array(password, counter, encryptedText);
}

function decrypt(encryptedText, counter, password) {
    const encryptedBytes = aesjs.utils.hex.toBytes(textToHex(encryptedText));
    const pwd = new buffer.SlowBuffer(password.slice(4, password.length).normalize('NFKC'));
    const salt = new buffer.SlowBuffer(password.slice(0, 4).normalize('NFKC'));
    const key = scrypt.syncScrypt(pwd, salt, 8, 256 / 8, 1, 32);
    const aesCtr = new aesjs.ModeOfOperation.ctr(key, new aesjs.Counter(Number(counter)));
    const decryptedBytes = aesCtr.decrypt(encryptedBytes);
    return aesjs.utils.utf8.fromBytes(decryptedBytes);
}