Great! Below is a well-structured and complete `README.md` tailored to your **ICS 4104 Load Balancer Assignment** project (`DockerTest`). You can paste this directly into your repo’s `README.md` file.

---

### ✅ Create or Edit the README File

```bash
nano README.md
```

Paste the following content:

---

# 🌀 ICS 4104: Distributed Systems - Load Balancer Project

This project implements a **customizable load balancer** using Docker and Python (Flask) as part of the ICS 4104 Distributed Systems assignment. It uses **consistent hashing** and can dynamically **spawn/remove server containers**, monitor heartbeat endpoints, and ensure even load distribution across replicas.

---

## 📦 Project Structure

```
DockerTest/
├── server/              # Minimal HTTP server code
│   ├── server.py
│   └── Dockerfile
├── loadbalancer/        # Load balancer logic with consistent hashing
│   ├── consistent_hash.py
│   ├── load_balancer.py
│   └── Dockerfile
├── docker-compose.yml   # Composition of the load balancer container
├── Makefile             # Commands for build, run, shutdown
└── README.md
```

---

## 🚀 Features

* Deploys a load balancer that handles requests from clients
* Routes requests to multiple backend servers using **consistent hashing**
* Supports **dynamic scaling**: `/add` and `/rm` endpoints
* Automatically **spawns new containers** from within a privileged container
* Handles server **failure detection** using `/heartbeat`
* Built with **Docker + Flask**

---

## ⚙️ Requirements

* Ubuntu 20.04+ with Docker and Docker Compose installed
* Python 3.10+
* Internet access to pull Docker base images

---

## 🧪 Setup & Deployment

### ✅ 1. Clone and Build the Project

```bash
git clone https://github.com/ShadrachAroni/DockerTest.git
cd DockerTest
make build
```

### ✅ 2. Start the Load Balancer

```bash
make up
```

---

## 🔍 API Endpoints

| Method | Endpoint | Description                                     |
| ------ | -------- | ----------------------------------------------- |
| GET    | `/rep`   | Returns list of active server replicas          |
| POST   | `/add`   | Adds server containers                          |
| DELETE | `/rm`    | Removes server containers                       |
| GET    | `/home`  | Routes to a random server using consistent hash |

---

## 📥 Example API Calls

### ➕ Add New Servers

```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"n": 2, "hostnames": ["S4", "S5"]}'
```

### ➖ Remove Servers

```bash
curl -X DELETE http://localhost:5000/rm \
  -H "Content-Type: application/json" \
  -d '{"n": 1, "hostnames": ["S4"]}'
```

### 🔁 View Replicas

```bash
curl http://localhost:5000/rep
```

### 🧭 Route Request

```bash
curl http://localhost:5000/home
```

---

## 🧠 Design Highlights

### 🔄 Consistent Hashing

* 512 slots
* 9 virtual nodes per server
* Custom hash functions for mapping requests and servers

### 🐳 Container Management

* The load balancer runs as a **privileged container**
* Spawns server containers using the host Docker daemon (`/var/run/docker.sock`)

---

## 📊 Performance Analysis (Task 4)

* **Test A-1**: 10,000 async requests sent with 3 replicas → near-even distribution
* **Test A-2**: Increased replicas from 2 to 6 → showed improved load balancing
* **Test A-3**: Simulated server failure → new instance automatically created
* **Test A-4**: Changed hash function → compared behavior and distribution

> Scripts and graphs for analysis are available in the `/analysis` folder (if included).

---

## ✍️ Contributors

* 👤 Shadrach Aroni

---

## 📎 References

* [Docker Docs](https://docs.docker.com/)
* [Consistent Hashing](https://web.stanford.edu/class/cs168/l/l1.pdf)
