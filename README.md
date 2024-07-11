# Vault agent

This agent demonstrates how to use the Cert auth method with HashiCorp Vault to synchronize secrets from a KV version 2 secrets engine to a local file using Python.

## Prerequisites
- You have installed Python 3.12+
- The machine running this agent must have access to the Vault server
- You have configured the KV version 2 secrets engine in Vault
- You have certificates for the Cert auth method in Vault

## Setup
```sh
# Clone the repository
git clone https://github.com/end-2/vault-agent.git
cd vault-agent

# Create a virtual environment and activate it
python3 -m venv .venv
source .venv/bin/activate

# Install the required python packages
pip install -r requirements.txt
```

## Usage
```sh
# Create a config file
cp config.yaml.example config.yaml

# Run
python3 vault-k8s-sync-secret.py
```

## Limitations
1. This project only supports the Cert authentication method.
2. This project only supports the KV version 2 secrets engine.
