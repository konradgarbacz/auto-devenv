# auto-devenv

Automated developer environment built with bash scripts on a fresh Ubuntu Server VM running in VMware Fusion. This is a hands-on learning project covering Linux, bash scripting, Docker, Git, and basic networking.

---

## What does this project do?

Three bash scripts that fully automate setting up a fresh VM:

1. Configure the system (hostname, user, packages)
2. Install Docker
3. Deploy a web app (nginx + PostgreSQL) in containers

After running the scripts, you have a working environment accessible from the host browser.

---

## Requirements

- VMware Fusion (macOS) with Ubuntu Server
- VM network set to **Bridged** (VM gets its own IP)
- SSH access from host to VM
- Git installed locally

---

## Project structure

```
devenv-project/
├── README.md
├── setup/
│   ├── 01-init-vm.sh         # system configuration
│   ├── 02-install-docker.sh  # Docker installation
│   └── 03-deploy-app.sh      # app deployment
├── docker/
│   ├── docker-compose.yml    # nginx + postgres
│   └── nginx/
│       └── default.conf
└── docs/
    └── network-diagram.md    # network diagram
```

---

## How to run

### 1. Clone the repo on the VM

```bash
git clone https://github.com/YOUR_USERNAME/devenv-project.git
cd devenv-project
```

### 2. Run the scripts in order

```bash
chmod +x setup/*.sh

sudo ./setup/01-init-vm.sh
sudo ./setup/02-install-docker.sh
./setup/03-deploy-app.sh
```

### 3. Verify it works

Open a browser on the host and go to:

```
http://YOUR_VM_IP:8080
```

You should see the nginx welcome page.

---

## Network diagram

```
[macOS Host]
     |
     | SSH :22 / HTTP :8080
     |
[VMware Fusion - Bridged]
     |
[Ubuntu Server VM]  192.168.x.x
     |
[Docker Network]  172.17.0.0/16
     |
     ├── nginx (port 8080)
     └── postgres (port 5432)
```

---

## Tech stack

| Technology | Purpose |

| VMware Fusion | virtual machine |
| Ubuntu Server 22.04 | VM operating system |
| Bash | automation scripts |
| Docker + Compose | containerized application |
| nginx | web server |
| PostgreSQL | database |
| Git + GitHub | version control |

---


