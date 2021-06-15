import express from 'express';
import {sessionIdEncrypter} from "./modules/sessionIdEncrypter";
const app = express()

const url = '/pdapsession';
const port = 3000;

app.get(url, sessionIdEncrypter)
app.listen(port,()=>console.log(`Session encrypter listening on http://localhost:${port}${url}`))