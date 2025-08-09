# browser_manager

**browser_manager** is a Python-based gRPC-powered browser control system. It provides a modular client-server architecture to manage browser operations like screenshots, accessibility inspections, command handling, and tracing using trace lens utilities.

---

## Features

- gRPC server and client interface (`browser_server.py`, `browser_client.py`)
- Protobuf definition and generated gRPC bindings (`.proto`, `*_pb2.py`, `*_pb2_grpc.py`)
- Command management framework (`command_manager.py`)
- Utilities for tracing (`trace_lens.py`), testing (`test_trace_lens.py`), and screenshot capture (`take_screenshot.py`)
- Integration tests and tools for accessibility checks (`get_accessibility_existing_browser.py`)
- Redis demo integration (`redis_test.py`)

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Installation](#installation)  
3. [Project Files Overview](#project-files-overview)  
4. [Usage](#usage)  
5. [Examples](#examples)  
6. [Contributing](#contributing)  
7. [License](#license)

---

## 1. Prerequisites

- Python 3.8+  
- `pip` for dependency management  
- Ensure `grpcio` and `protobuf` are installed (defined in `requirements.txt`)

---

## 2. Installation

```bash
git clone https://github.com/toutia/browser_manager.git
cd browser_manager
pip install -r requirements.txt
