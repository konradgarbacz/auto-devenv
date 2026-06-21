# Flask App with Docker and Nginx

Simple Flask REST API containerized with Docker and served behind Nginx reverse proxy.

## Tech Stack
- Python 3.12 / Flask
- Docker
- Nginx (reverse proxy)
- Bash (automation)

## Project Structure
bash-docker/
├── app.py
├── requirements.txt
├── Dockerfile
└── scripts/
    └── setup.sh

## How to run

Clone the repository:
git clone https://github.com/konradgarbacz/bash-docker.git
cd bash-docker

Run the setup script (installs Docker, Nginx, builds and starts the container):
bash scripts/setup.sh

## Endpoints
- GET / → returns JSON with status ok
- GET /health → returns JSON with health status

## How it works
User → port 80 (Nginx) → port 5000 (Flask container)