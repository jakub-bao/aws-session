import {execPython} from "./execPython";

export function encrypt(key:string, message:string):Promise<string>{
    return execPython(['../encrypter/fernetEncrypt.py',key, message])
}