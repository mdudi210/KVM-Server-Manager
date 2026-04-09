# KVM Server Manager - Nginx-First Deployment Guide

This guide deploys the app behind nginx as the single public entrypoint.
Backend and MySQL stay private inside the Docker network.

## Architecture

- Public: `nginx` on port `80`
- Private internal services: `frontend` (`8080` internal), `backend` (`8000` internal), `mysql` (`3306` internal)
- Browser auth: HTTP-only cookie set by backend, sent via same-origin requests through nginx

## Prerequisites

- Ubuntu 20.04+
- Docker + Docker Compose
- At least 4GB RAM and 20GB free disk

## 1) Firewall

Open only the nginx port:

```bash
sudo ufw allow 80/tcp
sudo ufw enable
sudo ufw status
```

If you terminate TLS externally (recommended for production), also open `443/tcp` on that external ingress/load balancer.

## 2) Configure Environment

Create/update your `.env` file before startup:

```env
# Database
DB_USER=kvm_user
DB_PASSWORD=change-me
DB_DATABASE=kvm_db
MYSQL_ROOT_PASSWORD=change-me-root

# JWT / auth
AUTHJWT_SECRET_KEY=change-this-to-a-long-random-secret
RETURN_TOKEN_IN_BODY=false

# Cookie settings
# Use false for plain HTTP, true when served over HTTPS
AUTHJWT_COOKIE_SECURE=false
AUTHJWT_COOKIE_SAMESITE=lax
AUTHJWT_COOKIE_CSRF_PROTECT=false

# CORS - explicit origins only (no *)
ALLOWED_ORIGINS=http://localhost,http://127.0.0.1
```

Production note:
- If app is served over HTTPS, set `AUTHJWT_COOKIE_SECURE=true`.
- Keep `ALLOWED_ORIGINS` explicit and minimal.

## 3) Start the Stack

```bash
docker compose up -d --build
docker compose ps
```

## 4) Validate Deployment

```bash
# nginx health
curl -i http://localhost/health

# app homepage through nginx
curl -i http://localhost/

# backend root through nginx proxy path
curl -i http://localhost/api/
```

Expected:
- `/health` returns `200 healthy`
- UI is reachable via nginx
- Backend APIs reachable via nginx routes (`/login`, `/vm`, `/api/*`, `/ws/*`)

## 5) Access

- Local: `http://localhost`
- Network: `http://YOUR_SERVER_IP`

Do not expose backend/mysql ports publicly. Use nginx as the only entrypoint.

## 6) Operations

```bash
# logs
docker compose logs -f
docker compose logs -f nginx
docker compose logs -f backend

# restart
docker compose restart

# stop
docker compose down
```

## 7) Security Defaults Already Applied

Current nginx config includes:
- Security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, CSP)
- Hidden file blocking
- Rate limiting on auth endpoints (`/login`, `/adlogin`, `/logout`)
- WebSocket proxy support (`/ws/*`)
- Static asset caching
- `server_tokens off`

## 8) HTTPS Recommendation

This compose stack serves HTTP by default. For production:
- Terminate TLS at cloud load balancer/reverse proxy or extend nginx with TLS certs.
- Then set `AUTHJWT_COOKIE_SECURE=true`.

## 9) Quick Troubleshooting

```bash
# render final compose config
docker compose config

# check running containers
docker ps

# inspect nginx logs
docker compose logs nginx
```

If UI loads but API fails, verify:
- backend container is healthy
- nginx routes include `/vm`, `/login`, `/adlogin`, `/logout`, `/ws/*`
- browser requests are same-origin and include cookies
