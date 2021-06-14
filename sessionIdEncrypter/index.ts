import express from 'express';
const app = express()

app.get('/pdapsession', async function (req, res) {
    res.send(req.headers)
})

app.listen(3000)