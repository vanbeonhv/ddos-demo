const http = require('http');
const server = http.createServer((req, res) => {
  console.log('Request received');
  res.end('Hello from Node.js \n');
});
server.listen(3000, () => console.log('Server running on port 3000'));