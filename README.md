# vps
Simple asyncio python3 webserver for my VPSs

# Pre Cert Chmod
```
chmod 755 /etc/letsencrypt/archive /etc/letsencrypt/live
```

# Docker Build
```
docker build --network=host --tag vps_web .
docker run --name web --hostname $(hostname) -p 80:6968 -p 443:6969 --mount type=bind,source=/etc/letsencrypt/,target=/etc/letsencrypt/,readonly vps_web
```
