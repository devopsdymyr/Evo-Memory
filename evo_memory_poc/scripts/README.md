# Scripts Directory

This directory contains utility scripts and test files for the Evo-Memory API.

## 📜 Scripts

### Setup
- **`setup.sh`** - Environment setup script
  - Creates virtual environment
  - Installs dependencies
  - Creates `.env` file template
  - Sets up required directories

  Usage:
  ```bash
  ./scripts/setup.sh
  ```

### Testing
- **`test_api_endpoints.py`** - Test business logic directly
  - Tests all service methods without starting server
  - No dependencies on running server
  - Fast execution for development

  Usage:
  ```bash
  python3 scripts/test_api_endpoints.py
  ```

- **`test_api_server.py`** - Test HTTP API endpoints
  - Tests all endpoints via HTTP requests
  - Requires server to be running
  - Validates full request/response cycle

  Usage:
  ```bash
  # Terminal 1: Start server
  python3 main.py

  # Terminal 2: Run tests
  python3 scripts/test_api_server.py
  ```

## 🧪 Running Tests

### Quick Test (Business Logic)
```bash
python3 scripts/test_api_endpoints.py
```

### Full Test (HTTP API)
```bash
# Start server in background or separate terminal
python3 main.py &

# Run HTTP tests
python3 scripts/test_api_server.py
```

## 📝 Notes

- All scripts should be run from the project root directory
- Test scripts use relative imports, so they must be run from root
- Setup script creates virtual environment in project root

