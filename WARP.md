# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

Logan is a load testing and chaos engineering toolkit consisting of:
- **Load Testing**: Python-based HTTP load testing framework with configurable test suites
- **Chaos Engineering**: Go-based HTTP attack tool and Vagrant-managed VM infrastructure for distributed testing

## Architecture

### Load Testing Component (Python)
- **Entry Point**: `main.py` - Interactive CLI for selecting and running load tests
- **Configuration**: `config.ini` - Global settings (app directory, max workers)
- **Test Definitions**: Located in `apps/{target}/{test_suite}/test_config.yaml`
- **Utilities**: `utils/helpers.py` - YAML parsing, logging, input sanitization

The load testing framework follows this flow:
1. User selects target application from `apps/` directory
2. System scans for available test suites within the target
3. User specifies number of runs
4. Concurrent HTTP requests are executed using ThreadPoolExecutor
5. Results are logged to `results.log` in the test suite directory

### Chaos Engineering Component
- **HTTP Attack Tool**: `chaos/http_attack/main.go` - Generates high-volume HTTP traffic (100MB POST payloads)
- **Infrastructure**: `chaos/zombies/Vagrantfile` - Creates 20 Ubuntu VMs for distributed attacks

## Common Commands

### Load Testing
```bash
# Run the main load testing interface
python main.py

# Direct execution (interactive prompts will follow)
cd /Users/netrunner/Desktop/dev/logan && python main.py
```

### Chaos Engineering
```bash
# Build and run HTTP attack tool
cd chaos/http_attack
go build
./http_attack -url="http://target.com" -verb="POST"

# Set up distributed VM infrastructure
cd chaos/zombies
vagrant up
vagrant ssh vm1
```

## Project Structure
```
logan/
├── main.py                    # Load testing CLI entry point
├── config.ini                 # Global configuration
├── apps/                      # Load test target definitions
│   └── {target}/              # Target application directory
│       └── {test_suite}/      # Test suite directory
│           └── test_config.yaml
├── chaos/
│   ├── http_attack/           # Go-based HTTP stress tool
│   └── zombies/               # Vagrant VM infrastructure
└── utils/
    └── helpers.py             # Shared utilities
```

## Test Configuration Format

Test configurations are YAML files with this structure:
```yaml
main:
  endpoint: "http://localhost:80/status/200"
  method: "POST"
  expected_status_code: 200
```

## Development Notes

- **Dependencies**: Python requires `requests`, `pyyaml`, `tqdm`. Go HTTP attack tool has no external dependencies.
- **Logging**: Results are automatically logged to `results.log` in each test suite directory
- **Concurrency**: Max workers configurable in `config.ini` (default: 20)
- **Input Validation**: All user inputs are sanitized via regex in `helpers.sanitize_input()`
- **Infrastructure**: Vagrant creates VMs with IPs 192.168.56.1-20 for distributed testing

## File Extensions and Languages
- `.py` - Python load testing framework
- `.go` - Go chaos engineering tools  
- `.yaml` - Test configuration files
- `Vagrantfile` - VM infrastructure definition