import {execPython} from "./execPython";

function parse(jsonResponse:string):string{
    return JSON.parse(jsonResponse).ENCRYPTION_KEY;
}

export async function getEncryptionKey():Promise<string>{
    return parse(await execPython(['../encryptionKey/getEncryptionKey.py']));
}