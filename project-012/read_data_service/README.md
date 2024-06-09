# How to play with Kong:
- create compose file with all services
- to run type 'docker compose --profile database up -d' and press enter
- Kong Ports are 8000, 8001 and 8002
- 8000 will be used for services, 8001 for admin activities and 8002 for Kong ui
- In Kong UI, add services, route, comsumer, credentials (if needed)
- to get Secret and Key from Kong UI, type 'localhost:8001/consumer-name/jwt' and run get/post reqyuest via Postman
- by providing these info, we get Access Token