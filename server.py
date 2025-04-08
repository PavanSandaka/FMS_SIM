import socket
import threading
import json

node_occupancy = {}  # node_id -> robot_name
lock = threading.Lock()

def handle_client(conn, addr):
    global node_occupancy
    robot_name = None

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            info = json.loads(data)
            robot_name = info['robot']
            current_node = info['current']
            next_node = info['next']

            with lock:
                # Mark current node as occupied
                node_occupancy[current_node] = robot_name

                # Check if next_node is already taken
                if node_occupancy.get(next_node) in [None, robot_name]:
                    response = {"action": "proceed"}
                else:
                    response = {"action": "wait"}

            conn.send(json.dumps(response).encode())
        except Exception as e:
            print(f"[ERROR] {e}")
            break

    with lock:
        if robot_name in node_occupancy.values():
            # Cleanup on disconnect
            keys_to_delete = [k for k, v in node_occupancy.items() if v == robot_name]
            for k in keys_to_delete:
                del node_occupancy[k]
    conn.close()

def start_server(host='localhost', port=9000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print(f"[SERVER] Listening on {host}:{port}")

    while True:
        conn, addr = s.accept()
        print(f"[CONNECTED] {addr}")
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
