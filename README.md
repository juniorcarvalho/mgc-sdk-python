# MGC SDK for Python

[![PyPI](https://img.shields.io/pypi/v/mgc-sdk-python)](https://pypi.org/)
[![Python](https://img.shields.io/pypi/pyversions/mgc-sdk-python)](https://pypi.org/)

An unofficial, open-source Python SDK for interacting with the Magalu Cloud API.

This project aims to provide a Pythonic and developer-friendly interface for Magalu Cloud services, inspired by the official Go SDK while remaining completely independent from Magalu Cloud and its maintainers. The project is community-driven and maintained by contributors.

> **Disclaimer**
>
> This is an unofficial SDK and is not affiliated with, endorsed by, or maintained by Magalu Cloud. For the official SDKs and tools, visit the Magalu Cloud GitHub organization.

## Features

- Pythonic API design
- Async support using `httpx`
- Typed Python interfaces
- Modular service architecture
- Easy authentication using API keys
- Open-source and community-driven
- Designed for automation, scripting, and backend applications

## Installation

### Using pip

```bash
pip install mgc-sdk-python
```

### Using uv

```bash
uv add mgc-sdk-python
```

### Development installation

```bash
git clone https://github.com/kayqueGovetri/mgc-sdk-python.git

cd mgc-sdk-python

make sync-dev
```

## Quick Start

```python
import asyncio

from mgc.client import Client


async def main() -> None:
    async with Client(api_key="YOUR_API_KEY") as client:
        virtual_machines = await client.compute.virtual_machines.list()

    print(virtual_machines)


if __name__ == "__main__":
    asyncio.run(main())
```

## Authentication

The SDK authenticates requests with a Magalu Cloud API key. Pass the key when
creating the client:

```python
from mgc.client import Client

client = Client(
    api_key="YOUR_API_KEY"
)
```

## Supported Services

Current implementation status:

### Compute

- [x] Virtual Machines
- [x] Images
- [x] Machine Types
- [x] Snapshots
- [x] Backups

### Block Storage

- [x] Volumes
- [ ] Snapshots
- [x] Volume type lookup

### Networking

- [ ] VPCs
- [ ] Subnets
- [ ] Security Groups
- [ ] Public IPs

### Kubernetes

- [ ] Clusters
- [ ] Node Pools

### Database

- [ ] DBaaS Instances
- [ ] Replicas
- [ ] Snapshots

> The roadmap evolves based on community contributions and API availability.

## Project Structure

```text
mgc-sdk-python/
├── examples/
│   ├── block_storage/
│   │   ├── snapshot/
│   │   └── volume/
│   └── compute/
│       ├── backup/
│       ├── images/
│       ├── snapshot/
│       └── virtual_machine/
├── src/
│   └── mgc/
│       ├── resources/
│       │   ├── block_storage/
│       │   │   ├── block_storage.py
│       │   │   ├── snapshots.py
│       │   │   └── volumes.py
│       │   └── compute/
│       │       ├── backups.py
│       │       ├── compute.py
│       │       ├── images.py
│       │       ├── machine_types.py
│       │       ├── snapshots.py
│       │       └── virtual_machines.py
│       ├── __init__.py
│       ├── auth.py
│       ├── client.py
│       ├── config.py
│       ├── exceptions.py
│       ├── region.py
│       └── transport.py
├── tests/
│   ├── resources/
│   │   ├── block_storage/
│   │   └── compute/
│   ├── conftest.py
│   ├── test_client.py
│   ├── test_config.py
│   ├── test_region.py
│   └── test_transport.py
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
```

## Why This Project?

While Magalu Cloud provides official tooling and SDKs, Python developers may prefer a native Python experience for:

- Automation
- Infrastructure management
- Data engineering
- Backend services
- Serverless applications
- Scripts and CLI tools

This project seeks to fill that gap with a modern Python SDK.

## Contributing

Contributions are welcome.

You can contribute by:

- Reporting bugs
- Suggesting new features
- Improving documentation
- Adding support for new services
- Writing tests

### Running tests

```bash
make test
```

### Linting

```bash
make lint
```

### Formatting check

```bash
make ruff-format-check
```

## Roadmap

- [ ] Full Compute API coverage
- [ ] Networking support
- [ ] Kubernetes support
- [ ] DBaaS support
- [ ] Object Storage support
- [ ] CLI integration
- [ ] Complete documentation
- [ ] Automated releases

## Related Projects

- Official Magalu Cloud Go SDK
- Official Magalu Cloud Organization

See the [LICENSE](LICENSE) file for details.

---

Built and maintained by the open-source community.
