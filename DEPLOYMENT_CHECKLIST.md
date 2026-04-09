# Deployment Checklist (Nginx-First)

Use this checklist before and after deployment.

## Pre-Deployment

- [ ] Ubuntu server ready (20.04+)
- [ ] Docker + Docker Compose installed
- [ ] Firewall opened for `80/tcp` (and `443/tcp` only if TLS terminates there)
- [ ] `.env` prepared with strong secrets (`AUTHJWT_SECRET_KEY`, DB passwords)
- [ ] `RETURN_TOKEN_IN_BODY=false` set
- [ ] `ALLOWED_ORIGINS` explicitly set (not `*`)

## Docker Deployment

- [ ] Run `docker compose up -d --build`
- [ ] All containers healthy: `docker compose ps`
- [ ] Nginx health check works: `curl http://localhost/health`
- [ ] Frontend loads through nginx: `http://SERVER_IP`

## Network Exposure

- [ ] Only nginx is publicly exposed
- [ ] Backend port `8000` is not exposed publicly
- [ ] MySQL port `3306` is not exposed publicly

## Security

- [ ] Default app users/passwords changed
- [ ] Cookie settings reviewed (`AUTHJWT_COOKIE_SECURE`, `AUTHJWT_COOKIE_SAMESITE`)
- [ ] HTTPS plan in place for production
- [ ] Backup strategy defined

## Functional Validation

- [ ] Login works (cookie-based session)
- [ ] VM list/state endpoints work via nginx
- [ ] WebSocket `/ws/vm-updates` works while logged in
- [ ] Logout invalidates session and redirects to login

## Post-Deployment

- [ ] Logs monitored (`docker compose logs -f`)
- [ ] Team has documented restart/recovery procedure
- [ ] Periodic update cadence scheduled
