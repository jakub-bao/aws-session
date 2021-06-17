import {getEncryptionKey} from "./getEncryptionKey";
import {encrypt} from "./encrypt";

export async function sessionIdEncrypter(req,res){
    try {
        let originalSessionId:string = req.headers.cookie;
        let encryptionKey:string = await getEncryptionKey();
        let encryptedSessionId = await encrypt(encryptionKey, originalSessionId);
        res.send(encryptedSessionId);
    } catch(e){
        res.status(500).send(e);
    }
}