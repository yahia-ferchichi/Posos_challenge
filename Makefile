
buildmodel:
	$(info Make: Building Model image.)
	@docker build -t mymodel -f Dockerfile .
	
runmodel:
	$(info Make: Running Model image.)
	@docker run -it mymodel
	
buildapi:
	$(info Make: Building API image.)
	@docker build -t myapi -f API/Dockerfile .
	
runapi:
	$(info Make: Running API image.)
	@docker run -it -p 4002:8000 myapi
	

clean:
	@docker system prune --volumes --force


