DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = main-app

.PHONY: app down app-shell app-logs
app:
	${DC} -p dit -f ${APP_FILE} ${ENV} up --build -d

down:
	${DC} -p dit -f ${APP_FILE} ${ENV} down

app-shell:
	${EXEC} ${APP_CONTAINER} bash

app-logs:
	${LOGS} ${APP_CONTAINER} -f
