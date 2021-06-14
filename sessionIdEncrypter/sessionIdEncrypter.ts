import {spawn} from "child_process";

async function getEncryptionKey():Promise<string>{
    return new Promise((resolve,reject)=>{
        let python = spawn('python3',['../encryptionKey/getEncryptionKey.py'])
        python.stdout.on('data',(data)=>{
            resolve(data);
        })
        python.stderr.on('data',(data)=>{
            reject(`Cannot communicate with PYTHON ${data}`);
        })
    });
}

export async function sessionIdEncrypter(req,res){
    try {
        let encryptionKey = await getEncryptionKey();
        res.send({cookie: req.headers.cookie, encryptionKey});
    } catch(e){
        res.status(500).send(e);
    }
}