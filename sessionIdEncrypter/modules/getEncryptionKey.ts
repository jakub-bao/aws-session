import {spawn} from "child_process";

function parse(jsonResponse:string):string{
    return JSON.parse(jsonResponse).ENCRYPTION_KEY;
}

export async function getEncryptionKey():Promise<string>{
    return new Promise((resolve,reject)=>{
        let python = spawn('python3',['../encryptionKey/getEncryptionKey.py'])
        python.stdout.on('data',(data:Buffer)=>{
            let asString = data.toString();
            resolve(parse(asString));
        })
        python.stderr.on('data',(data)=>{
            reject(`Cannot communicate with PYTHON ${data}`);
        })
    });
}