up:
	docker compose up -d --build
down:
	docker compose down -v
logs:
	docker compose logs -f gateway orders payments
break-payments:
	./scripts/chaos.sh payments latency 1500
fail-orders:
	./scripts/chaos.sh orders errors 0.4
heal:
	@for s in gateway orders payments; do ./scripts/chaos.sh $$s reset; done
