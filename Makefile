# Makefile
.PHONY: help build up down restart logs clean test install

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

help:
	@echo ""
	@echo "${GREEN}DokPDF - Kelola PDF Jadi Mudah${RESET}"
	@echo "${YELLOW}Available commands:${RESET}"
	@echo ""
	@echo "  ${WHITE}make build${RESET}     - Build Docker images"
	@echo "  ${WHITE}make up${RESET}        - Start all containers"
	@echo "  ${WHITE}make down${RESET}      - Stop all containers"
	@echo "  ${WHITE}make restart${RESET}   - Restart all containers"
	@echo "  ${WHITE}make logs${RESET}      - View logs"
	@echo "  ${WHITE}make clean${RESET}     - Clean up containers and images"
	@echo "  ${WHITE}make test${RESET}      - Test API endpoints"
	@echo "  ${WHITE}make install${RESET}   - Install dependencies locally"
	@echo ""

build:
	@echo "${GREEN}Building DokPDF Docker images...${RESET}"
	docker-compose build

up:
	@echo "${GREEN}Starting DokPDF containers...${RESET}"
	docker-compose up -d
	@echo ""
	@echo "${GREEN}✅ DokPDF is running!${RESET}"
	@echo "${YELLOW}📱 Frontend: http://localhost:8080${RESET}"
	@echo "${YELLOW}🔧 API: http://localhost:5000${RESET}"
	@echo "${YELLOW}📊 Logs: make logs${RESET}"

down:
	@echo "${YELLOW}Stopping DokPDF containers...${RESET}"
	docker-compose down

restart:
	@echo "${YELLOW}Restarting DokPDF containers...${RESET}"
	docker-compose restart

logs:
	@echo "${YELLOW}Showing logs (Ctrl+C to exit)...${RESET}"
	docker-compose logs -f

clean:
	@echo "${YELLOW}Cleaning up...${RESET}"
	docker-compose down -v
	docker system prune -f
	rm -rf uploads/temp/*
	@echo "${GREEN}Cleanup complete!${RESET}"

test:
	@echo "${YELLOW}Testing DokPDF API...${RESET}"
	@curl -s http://localhost:5000/api/health | python -m json.tool || echo "${RED}API not responding${RESET}"
	@echo ""
	@echo "${GREEN}✅ API is healthy${RESET}"

install:
	@echo "${YELLOW}Installing Python dependencies...${RESET}"
	cd api && pip install -r requirements.txt
	@echo "${GREEN}Installation complete!${RESET}"