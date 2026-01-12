# KVM Server Manager - Deployment Guide

This guide covers deploying the KVM Server Manager application on an Ubuntu server accessible via your company network with SSL support.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Network Configuration](#network-configuration)
3. [SSL Certificate Setup](#ssl-certificate-setup)
4. [Docker Deployment](#docker-deployment)
5. [Accessing the Application](#accessing-the-application)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- Ubuntu 20.04 or later
- Docker and Docker Compose installed
- At least 4GB RAM
- At least 20GB free disk space
- Network access from other machines in your company network

### Install Docker and Docker Compose

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (logout/login required)
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

## Network Configuration

### 1. Find Your Server IP Address

```bash
# Find your IP address
ip addr show | grep "inet " | grep -v 127.0.0.1

# Or use
hostname -I
```

**Note the IP address** (e.g., `192.168.1.100`) - you'll use this to access the application.

### 2. Configure Firewall (UFW)

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# If you need direct access to backend (optional)
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 3. Configure Docker to Bind to All Interfaces

Docker containers are already configured to bind to `0.0.0.0`, which allows access from any network interface.

## SSL Certificate Setup

### Option 1: Self-Signed Certificate (Quick Setup)

For internal network use, you can generate a self-signed certificate:

```bash
# Navigate to project directory
cd /path/to/KVM-Server-Manager

# Generate SSL certificate
./scripts/generate-ssl.sh kvm-server.local ./nginx/ssl

# Verify certificates were created
ls -la nginx/ssl/
```

**Note:** Browsers will show a security warning for self-signed certificates. Users need to click "Advanced" and "Proceed anyway" the first time.

### Option 2: Let's Encrypt Certificate (Recommended for Production)

If you have a domain name pointing to your server:

```bash
# Install certbot
sudo apt install certbot -y

# Generate certificate (replace with your domain)
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to nginx/ssl directory
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./nginx/ssl/key.pem
sudo chmod 644 ./nginx/ssl/cert.pem
sudo chmod 600 ./nginx/ssl/key.pem

# Set up auto-renewal (optional)
sudo certbot renew --dry-run
```

### Option 3: Internal CA Certificate (Best for Company Networks)

For a proper internal certificate authority:

1. Set up an internal CA on a trusted server
2. Generate certificates signed by your CA
3. Distribute CA certificate to all company machines
4. Place certificates in `nginx/ssl/` directory

## Docker Deployment

### 1. Clone/Transfer Project Files

Ensure all project files are on your Ubuntu server.

### 2. Generate SSL Certificates (if not done already)

```bash
./scripts/generate-ssl.sh kvm-server.local ./nginx/ssl
```

### 3. Start the Application

```bash
# Build and start all containers
docker-compose up -d --build

# Check container status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Verify Services are Running

```bash
# Check all containers are up
docker ps

# Test backend health
curl http://localhost:8000/

# Test nginx
curl http://localhost/health
```

## Accessing the Application

### From the Server Itself

- **HTTP (redirects to HTTPS):** http://localhost
- **HTTPS:** https://localhost
- **Direct Backend API:** http://localhost:8000

### From Other Machines in Your Network

Replace `YOUR_SERVER_IP` with your actual server IP address:

- **HTTPS:** https://YOUR_SERVER_IP
- **HTTP (redirects to HTTPS):** http://YOUR_SERVER_IP
- **Direct Backend API:** http://YOUR_SERVER_IP:8000

**Example:** If your server IP is `192.168.1.100`:
- Access UI: https://192.168.1.100
- API: http://192.168.1.100:8000

### First-Time SSL Certificate Warning

When using a self-signed certificate:
1. Browser will show "Your connection is not private"
2. Click "Advanced" or "Show Details"
3. Click "Proceed to [IP] (unsafe)" or "Accept the Risk and Continue"

### Default Login Credentials

- **Admin:** `admin` / `password123`
- **Test User:** `testuser` / `password123`

**⚠️ IMPORTANT:** Change these passwords in production!

## Managing the Application

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql
docker-compose logs -f nginx
```

### Stop the Application

```bash
docker-compose down
```

### Restart the Application

```bash
docker-compose restart
```

### Update the Application

```bash
# Pull latest code
git pull  # or update files manually

# Rebuild and restart
docker-compose up -d --build
```

### Backup Database

```bash
# Create backup
docker exec kvm-mysql mysqldump -u kvm_user -pkvm_password kvm_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker exec -i kvm-mysql mysql -u kvm_user -pkvm_password kvm_db < backup_file.sql
```

## Troubleshooting

### Containers Won't Start

```bash
# Check logs
docker-compose logs

# Check if ports are already in use
sudo netstat -tulpn | grep -E ':(80|443|8000|3306)'

# Remove old containers and start fresh
docker-compose down -v
docker-compose up -d --build
```

### Cannot Access from Network

1. **Check firewall:**
   ```bash
   sudo ufw status
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

2. **Check server IP:**
   ```bash
   hostname -I
   ```

3. **Test connectivity from another machine:**
   ```bash
   ping YOUR_SERVER_IP
   curl http://YOUR_SERVER_IP/health
   ```

4. **Check Docker network:**
   ```bash
   docker network ls
   docker network inspect kvm-server-manager_kvm-network
   ```

### SSL Certificate Issues

```bash
# Verify certificates exist
ls -la nginx/ssl/

# Check nginx logs
docker-compose logs nginx

# Regenerate certificates
./scripts/generate-ssl.sh kvm-server.local ./nginx/ssl
docker-compose restart nginx
```

### Database Connection Issues

```bash
# Check MySQL is running
docker-compose ps mysql

# Check MySQL logs
docker-compose logs mysql

# Test MySQL connection
docker exec -it kvm-mysql mysql -u kvm_user -pkvm_password kvm_db
```

### Backend API Not Responding

```bash
# Check backend logs
docker-compose logs backend

# Test backend directly
curl http://localhost:8000/

# Restart backend
docker-compose restart backend
```

## Performance Tuning

### Increase Container Resources

Edit `docker-compose.yml` and add resource limits:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Database Optimization

For production, consider:
- Increasing MySQL buffer pool size
- Adding database indexes
- Setting up database replication

## Security Recommendations

1. **Change Default Passwords:**
   - Update database passwords in `docker-compose.yml`
   - Change default user passwords in the application

2. **Use Strong SSL Certificates:**
   - Prefer Let's Encrypt or internal CA over self-signed

3. **Restrict Network Access:**
   - Use firewall rules to limit access to specific IP ranges
   - Consider VPN for remote access

4. **Regular Updates:**
   - Keep Docker images updated
   - Apply security patches regularly

5. **Backup Strategy:**
   - Set up automated database backups
   - Store backups securely

## Frontend API Configuration

The frontend currently uses hardcoded API URLs. For production deployment:

### Option 1: Update Frontend Code (Recommended)

Update the frontend to use the new API configuration:

1. The frontend now includes `src/config/api.js` which can be configured
2. For production builds, update API calls to use relative URLs
3. Or set `VUE_APP_API_URL` environment variable before building

### Option 2: Use Nginx Proxy (Current Setup)

The nginx configuration handles API routes automatically. However, the frontend code needs to be updated to use relative URLs or the nginx proxy path.

**Quick Fix:** Update frontend API calls from:
```javascript
axios.post("http://127.0.0.1:8000/login", ...)
```

To:
```javascript
axios.post("/login", ...)  // Relative URL - uses same origin
```

Or use the API config helper:
```javascript
import { API_BASE_URL } from '@/config/api';
axios.post(`${API_BASE_URL}/login`, ...)
```

### Option 3: Build with Environment Variable

```bash
# Set API URL before building
export VUE_APP_API_URL=https://YOUR_SERVER_IP
cd frontend
npm run build
```

## Next Steps

- See [KUBERNETES_DEPLOYMENT.md](./KUBERNETES_DEPLOYMENT.md) for Kubernetes deployment
- Configure monitoring and logging
- Set up automated backups
- Implement CI/CD pipeline
- Update frontend API calls to use relative URLs or environment variables