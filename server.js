const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Python trading bot backend project');
});

server.listen(3000, () => {
  console.log('Dummy dev server running on http://localhost:3000');
});
