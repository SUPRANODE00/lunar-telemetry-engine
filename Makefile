.PHONY: sync push status

sync:
	git add run_capsule_node.py capsule_identity.toml .gitignore Makefile
	@git commit -m "auto(sync): update telemetry daemon state and automation at $(shell date -u +'%Y-%m-%d %H:%M:%S UTC')" || echo "No changes to commit"
	git push origin feat/stateless-control-plane

status:
	curl -s http://127.0.0.1:8080/status | jq .
