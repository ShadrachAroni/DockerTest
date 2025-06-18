from flask import Flask, request, jsonify
from consistent_hash import ConsistentHash
import docker
import random
import os

app = Flask(__name__)
client = docker.from_env()

hash_ring = ConsistentHash()
N = 3
replicas = []

def start_server(name):
    # If container already exists, remove it
    try:
        existing = client.containers.get(name)
        print(f"Removing existing container {name}...")
        existing.stop()
        existing.remove()
    except docker.errors.NotFound:
        pass

    container = client.containers.run(
        "server-image",
        name=name,
        environment={"SERVER_ID": name},
        network="net1",
        hostname=name,
        detach=True
    )
    hash_ring.add_server(name)
    replicas.append(name)


def stop_server(name):
    try:
        container = client.containers.get(name)
        container.stop()
        container.remove()
    except:
        pass
    hash_ring.remove_server(name)
    replicas.remove(name)

@app.route("/rep", methods=["GET"])
def get_replicas():
    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"})

@app.route("/add", methods=["POST"])
def add_replicas():
    data = request.json
    n = data.get("n", 0)
    names = data.get("hostnames", [])
    if len(names) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than newly added instances", "status": "failure"}), 400
    for i in range(n):
        name = names[i] if i < len(names) else f"Server{random.randint(100,999)}"
        start_server(name)
    return get_replicas()

@app.route("/rm", methods=["DELETE"])
def remove_replicas():
    data = request.json
    n = data.get("n", 0)
    names = data.get("hostnames", [])
    if len(names) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than removable instances", "status": "failure"}), 400
    for name in names[:n]:
        if name in replicas:
            stop_server(name)
    extra = n - len(names)
    for _ in range(extra):
        if replicas:
            stop_server(random.choice(replicas))
    return get_replicas()

@app.route("/<path:path>", methods=["GET"])
def route_request(path):
    key = random.randint(100000, 999999)
    server = hash_ring.get_server(key)
    if not server:
        return jsonify({"message": "No servers available", "status": "failure"}), 503
    try:
        container = client.containers.get(server)
        ip = container.attrs['NetworkSettings']['Networks']['net1']['IPAddress']
        import requests
        r = requests.get(f"http://{ip}:5000/{path}")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"message": str(e), "status": "failure"}), 500

if __name__ == "__main__":
    for i in range(1, N + 1):
        start_server(f"Server{i}")
    app.run(host="0.0.0.0", port=5000)
