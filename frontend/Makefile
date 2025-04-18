.PHONY: install dev build start lint clean

# Install dependencies
install:
	npm install

# Run development server
dev:
	npm run dev

# Build the application
build:
	npm run build

# Start production server
start:
	npm run start

# Run linting
lint:
	npm run lint

# Clean build artifacts and dependencies
clean:
	rm -rf .next
	rm -rf node_modules
	rm -f package-lock.json

# Default target
all: install build 