all:
	@docker compose -f docker-compose.yml up

clean:
	@docker compose -f docker-compose.yml down

fclean: clean
	@git clean -dfX
	@rm -f backend/users/migrations/0*.py

re: fclean all

prune: fclean
	@docker system prune -af

.PHONY: all clean fclean re prune
