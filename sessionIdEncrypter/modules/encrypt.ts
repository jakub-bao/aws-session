import {execPython} from "./execPython";

export function encrypt(key:string, message:string):Promise<string>{
    return execPython(['../encrypt/fernet',key, message])
}