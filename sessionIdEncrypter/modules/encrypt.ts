import Cryptr from 'cryptr';

export const encrypt = (key:string, message:string)=>{
    const cryptr = new Cryptr(key);
    return cryptr.encrypt(message);
}