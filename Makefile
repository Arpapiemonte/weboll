all: init.dev up.dev

init.dev:
	@echo "😎 Copying .env.example into .env ..."
	cp -fi .env.example .env
	@echo "📅 Shifting the dates of the preload data ..."
	./shift_dates.sh
	@echo "☮ Init done"

up.dev:
	@echo "▶ Starting local services ..."
	docker-compose -f local.yml up

build.dev:
	@echo "⚙ Building dev images with compose ..."
	docker-compose -f local.yml build --no-cache

down.dev:
	@echo "⏸ Stopping local services ..."
	docker-compose -f local.yml down

shutdown.dev:
	@echo "⏹ Stopping local services and tearing down the DB ..."
	docker-compose -f local.yml down -v