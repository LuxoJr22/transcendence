all:
	@docker compose -f docker-compose.yml up

clean:
	@docker compose -f docker-compose.yml down

fclean: clean
#	@docker run -it -v ./:/trans alpine rm -rf /trans/database # Used for delete database folder at school
	@git clean -dfX
	@rm -f backend/users/migrations/0*.py

re: clean all

prune: fclean
	@docker system prune -af
	@find backend/media/profile_pictures/ -type f ! -name 'default.jpg' -delete
	@find backend/media/profile_pictures/ -type d -empty -delete

.PHONY: all clean fclean re prune
