import {spawn} from "child_process";

async function getEncryptionKey():Promise<string>{
    return new Promise((resolve,reject)=>{
        let python = spawn('python3',['../encryptionKey/getEncryptionKey.py'])
        python.stdout.on('data',(data)=>{
            resolve(data.toString());
        })
        python.stderr.on('data',(data)=>{
            reject(`Cannot communicate with PYTHON ${data}`);
        })
    });
}

function parse(jsonResponse:string):string{
    return JSON.parse(jsonResponse).ENCRYPTION_KEY;
}

export async function sessionIdEncrypter(req,res){
    try {
        let encryptionKey = await getEncryptionKey().then(parse);
        res.send({cookie: req.headers.cookie, encryptionKey});
    } catch(e){
        res.status(500).send(e);
    }
}