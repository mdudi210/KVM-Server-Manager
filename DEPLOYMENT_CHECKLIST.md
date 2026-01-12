# Deployment Checklist

Use this checklist to ensure a successful deployment.

## Pre-Deployment

- [ ] Ubuntu server ready (20.04+)
- [ ] Docker installed and user added to docker group
- [ ] Docker Compose installed
- [ ] Server IP address noted
- [ ] Firewall configured (ports 80, 443)
- [ ] SSL certificates generated or obtained

## Docker Deployment

- [ ] Project files copied to server
- [ ] SSL certificates in `nginx/ssl/` directory
- [ ] `docker-compose.yml` reviewed and configured
- [ ] Database passwords changed (if needed)
- [ ] Run `docker-compose up -d --build`
- [ ] All containers running: `docker-compose ps`
- [ ] Application accessible via HTTPS
- [ ] Default passwords changed

## Kubernetes Deployment

- [ ] Kubernetes cluster ready
- [ ] `kubectl` configured and working
- [ ] Docker images built and pushed to registry
- [ ] SSL certificates created as Kubernetes secrets
- [ ] Storage class configured for MySQL
- [ ] All manifests applied: `kubectl apply -k k8s/`
- [ ] All pods running: `kubectl get pods -n kvm-server`
- [ ] Services accessible
- [ ] Ingress configured (if using)

## Network Access

- [ ] Server accessible from network: `ping SERVER_IP`
- [ ] HTTP redirects to HTTPS
- [ ] HTTPS accessible from other machines
- [ ] SSL certificate accepted (or warning acknowledged)
- [ ] Frontend loads correctly
- [ ] Backend API responds

## Security

- [ ] Default passwords changed
- [ ] Firewall rules configured
- [ ] SSL certificates valid
- [ ] Database credentials secure
- [ ] Regular backups configured

## Testing

- [ ] Login works with admin credentials
- [ ] API endpoints respond correctly
- [ ] Frontend-backend communication works
- [ ] Database persists data
- [ ] Application survives container restart

## Production Readiness

- [ ] Monitoring configured
- [ ] Logging configured
- [ ] Backup strategy in place
- [ ] Update procedure documented
- [ ] Disaster recovery plan ready
- [ ] Team trained on deployment

## Post-Deployment

- [ ] Documentation updated
- [ ] Access credentials secured
- [ ] Monitoring alerts configured
- [ ] Backup schedule verified
- [ ] Performance baseline established
