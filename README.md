# vps
Simple asyncio python3 webserver for my VPSs

# Docker Build
```
docker build --network=host --tag vps_web
docker run --name web -p 80:6969 vps_web
```
