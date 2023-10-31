# simbirgo

Swagger:

http://127.0.0.1:8000/docs

Runing:

1. `docker network create simbirgo_simbirgo-network`
2. `docker compose up database -d`
3. `docker build -t simbirgo-monolit --target slim .`
4. `docker run --network host simbirgo-monolit monolit database migrations migrate`
5. `docker run --network host -p "8000:8000" simbirgo-monolit monolit run`

Or

1. `sh ./start.sh`
