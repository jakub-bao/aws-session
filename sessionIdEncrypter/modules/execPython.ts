import {spawn} from "child_process";

export async function execPython(params:string[]):Promise<string>{
    return new Promise((resolve,reject)=>{
        let python = spawn('python3',params)
        python.stdout.on('data',(data:Buffer)=>{
            let asString = data.toString().replace(/\n/,'');
            resolve(asString);
        })
        python.stderr.on('data',(data)=>{
            reject(`Cannot communicate with PYTHON ${data}`);
        })
    });
}