# Start project

### Create .env
```
DB_USER=
DB_PASS=
DB_HOST=
DB_PORT=
DB_NAME=
DB_URL=postgresql+asyncpg://{}:{}@{}:{}/{} # for postgres with asyncpg
```
### Create dir certs and gen keys there
```bash
mkdir certs
cd certs

openssl genrsa -out jwt-private.pem 2048

openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

cd ..
```

### Start
```shell
python -m src.main
```
