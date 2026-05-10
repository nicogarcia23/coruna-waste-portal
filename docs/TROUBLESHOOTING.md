# Troubleshooting Guide

## Docker Hub TLS Certificate Errors

### Symptom
When running `make up all` or `docker compose up`, you see errors like:
```
failed to copy: httpReadSeeker: failed open: failed to do request: 
Get "https://docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com/...":
tls: failed to verify certificate: x509: certificate is not valid for any names
```

### Cause
This is a temporary connectivity issue with Docker Hub's Cloudflare CDN. It can be caused by:
- Temporary DNS or network issues
- Docker daemon cache issues
- Cloudflare CDN temporary outages
- Time synchronization issues

### Solutions (in order of effectiveness)

#### 1. **Restart Docker Daemon** (Recommended)
```bash
# On Linux
sudo systemctl restart docker

# On macOS with Docker Desktop
# Click Docker icon in menu bar > Restart

# On Windows with Docker Desktop
# Right-click Docker icon > Restart
```

#### 2. **Clear Docker Cache and Retry**
```bash
# Remove all stopped containers
docker container prune -f

# Remove dangling images
docker image prune -f

# Retry pulling
cd coruna-waste-portal
make up all
```

#### 3. **Verify Time Synchronization**
```bash
# Check if NTP is synced
timedatectl

# If not synced, sync manually (Linux)
sudo timedatectl set-ntp true
```

#### 4. **Pull Images Individually**
If `make up all` still fails, try pulling base images individually to identify which ones have issues:
```bash
docker pull redis:7-alpine
docker pull mongo:7
docker pull eclipse-mosquitto:2
docker pull fiware/orion-ld:1.6.0
docker pull orchestracities/quantumleap:latest
docker pull curlimages/curl:latest
docker pull grafana/grafana:latest
docker pull fiware/iotagent-ul:latest
docker pull ghcr.io/vroom-project/vroom-docker:latest
docker pull timescale/timescaledb-ha:pg16-all
```

#### 5. **Use Docker Desktop with Built-in Retry**
```bash
# Docker will auto-retry failed pulls
make up all
# Wait 5-10 minutes for retries
```

#### 6. **Change Docker DNS** (for WSL/Docker Desktop)
If you're using Docker Desktop on Windows with WSL:

1. Open Docker Desktop settings → Resources → Network
2. Check "Use a fixed gateway IP"  
3. Change DNS server to `8.8.8.8` (Google) or `1.1.1.1` (Cloudflare)
4. Click "Apply & Restart"

Or edit `~/.docker/daemon.json`:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"]
}
```

Then restart Docker Desktop from Windows (right-click → Restart).

#### 7. **Restart Docker Desktop Properly** (for WSL/Windows)
```bash
# From Windows PowerShell (as Administrator):
Restart-Service com.docker.service

# Or from WSL terminal:
# Click Docker icon → Restart

# Verify Docker is running:
docker ps
```

#### 8. **Check WSL Network Configuration**
If using WSL, verify nameserver:
```bash
cat /etc/resolv.conf
# Should show: nameserver 8.8.8.8 or similar

# If not, edit /etc/wsl.conf
sudo nano /etc/wsl.conf
# Add or modify:
[interop]
appendWindowsPath = true
```

#### 9. **Wait and Retry Later**
Sometimes Docker Hub CDN has temporary outages. Wait 15-30 minutes and retry:
```bash
sleep 1800  # Wait 30 minutes
make up all
```

## Docker Desktop on WSL/Windows Specific Issues

### Docker Service Not Found Error
**Error:** `Failed to restart docker.service: Unit docker.service not found`

**Cause:** You're using Docker Desktop (managed from Windows), not systemd service.

**Solution:** Restart Docker Desktop from Windows:
1. Right-click Docker icon in system tray (bottom right)
2. Select "Restart"
3. Wait 30 seconds for Docker to restart
4. Return to WSL terminal and retry: `make up all`

Or use PowerShell:
```powershell
# From Windows PowerShell as Administrator:
Restart-Service com.docker.service
# Then in WSL:
cd ~/coruna-waste-portal && make up all
```

### TLS Certificate Verification Errors from Docker Hub
**Error:** 
```
failed to copy: httpReadSeeker: failed open: failed to do request:
tls: failed to verify certificate: x509: certificate is not valid
```

**Cause:** Docker Hub CDN (Cloudflare) certificate issue, often related to network/DNS from WSL.

**Quick Fix:**
1. Restart Docker Desktop from Windows (see above)
2. Wait 2-3 minutes
3. Retry in WSL: `make up all`

**If that doesn't work:**
1. Open Docker Desktop → Settings → Resources → Network
2. Uncheck then recheck "Use a fixed gateway IP"
3. Change DNS to `8.8.8.8` (Google) 
4. Click "Apply & Restart"
5. Return to WSL and try again

## Orion LD Crashes with MongoDB 7 Compatibility Error

### Symptom
Orion LD container exits with error:
```
Unsupported OP_QUERY command: listDatabases
terminate called after throwing an instance of 'mongo::MsgAssertionException'
what(): field not found, expected type 4
```

### Cause
Orion LD 1.6.0 uses an older MongoDB driver that uses the deprecated **OP_QUERY** protocol. MongoDB 7.0+ removed support for OP_QUERY and only supports the newer **OP_MSG** protocol. This driver incompatibility causes Orion to crash on startup.

### Solution
Use MongoDB 5.0 instead of 7.x. Edit [infra/docker-compose.yml](../infra/docker-compose.yml):

```yaml
mongodb:
   image: mongo:5.0  # Change from mongo:7 to mongo:5.0
  restart: unless-stopped
  # ... rest of config
```

Then restart all services:
```bash
make down
make up all
```

## Services Not Starting

### Symptom
`make ps` shows no services running.

### Solutions
1. Check if all images pulled successfully:
   ```bash
   docker image ls | grep -E "redis|mongo|mosquitto|orion|quantumleap"
   ```

2. View detailed logs:
   ```bash
   make logs
   ```

3. Check specific service logs:
   ```bash
   docker compose -f infra/docker-compose.yml logs orion-ld
   docker compose -f infra/docker-compose.yml logs mongodb
   ```

4. Ensure .env file exists:
   ```bash
   ls infra/.env
   # If missing:
   cp infra/.env.example infra/.env
   ```

## Backend Not Connecting to Services

### Symptom
Backend starts but can't reach Orion, QuantumLeap, or Redis.

### Solutions
1. Verify services are running:
   ```bash
   make ps
   ```

2. Check network connectivity:
   ```bash
   docker compose -f infra/docker-compose.yml exec backend-api \
     curl -v http://orion-ld:1026/version
   ```

3. Verify environment variables in [infra/docker-compose.yml](../infra/docker-compose.yml):
   ```yaml
   ORION_LD_URL: http://orion-ld:1026
   REDIS_URL: redis://redis:6379/0
   ```

## Frontend Not Accessible

### Symptom
Frontend runs but shows blank page or connection errors.

### Solutions
1. Check if frontend is running:
   ```bash
   make ps
   curl -I http://localhost:3000
   ```

2. Check frontend logs:
   ```bash
   docker compose -f infra/docker-compose.yml logs frontend
   ```

3. Verify API endpoint:
   ```bash
   # In browser console, check:
   console.log(process.env.REACT_APP_API_URL || 'http://localhost:8000')
   ```

## Database Connection Issues

### Symptom
Database errors or connection timeouts.

### Solutions
1. Check TimescaleDB is running:
   ```bash
   docker compose -f infra/docker-compose.yml exec timescaledb \
     pg_isready -U waste -d waste
   ```

2. Check MongoDB is running:
   ```bash
   docker compose -f infra/docker-compose.yml exec mongodb \
     mongosh --eval "db.adminCommand('ping')"
   ```

3. Check credentials in [infra/.env](../infra/.env):
   ```
   POSTGRES_USER=waste
   POSTGRES_PASSWORD=waste-dev-password
   POSTGRES_DB=waste
   ```

## Port Conflicts

### Symptom
"Address already in use" errors when starting services.

### Solutions
```bash
# Find what's using the port (example: port 8000)
sudo lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different ports in infra/.env
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

## Need More Help?

1. Check logs: `make logs`
2. Check running processes: `make ps`
3. Review [README.md](../README.md) for setup steps
4. Check [docs/architecture.md](./architecture.md) for system overview
