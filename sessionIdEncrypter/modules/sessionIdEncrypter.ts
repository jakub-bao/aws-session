import {getEncryptionKey} from "./getEncryptionKey";

export async function sessionIdEncrypter(req,res){
    try {
        let encryptionKey = await getEncryptionKey();
        res.send({cookie: req.headers.cookie, encryptionKey});
    } catch(e){
        res.status(500).send(e);
    }
}