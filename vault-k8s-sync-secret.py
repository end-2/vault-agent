import time
import requests
import yaml
import json

class Vault:
    def __init__(self, config):
        self.url = config.get('url', 'https://localhost:8200')
        self.ca_cert = config.get('ca_cert', 'ca-cert.pem')
        self.login_path = config.get('login_path', 'cert')
        self.login_name = config.get('login_name', 'name')
        self.login_cert_path = config.get('login_cert_path', 'cert.pem')
        self.login_key_path = config.get('login_key_path', 'key.pem')
        self.kv_mount = config.get('kv_mount', 'kv')
        self.kv_path = config.get('kv_path', 'secret/data/path')

    def login(self):
        login_url = f'{self.url}/v1/auth/{self.login_path}/login'
        login_payload = {
            'name': self.login_name
        }

        response = requests.post(
            login_url,
            json=login_payload,
            verify=self.ca_cert,
            cert=(self.login_cert_path, self.login_key_path)
        )

        if response.status_code != 200:
            raise Exception(f'Failed to login to Vault: {response.text}')
        
        self.token = response.json().get('auth', {}).get('client_token', None)
        if not self.token:
            raise Exception(f'Failed to get token from Vault: {response.text}')
    
    def get_secret_data(self):
        secret_url = f'{self.url}/v1/{self.kv_mount}/data/{self.kv_path}'
        response = requests.get(
            secret_url,
            headers={
                'X-Vault-Token': self.token
            },
            verify=self.ca_cert,
        )

        if response.status_code != 200:
            raise Exception(f'Failed to get secret from Vault: {response.text}')
        
        secret_data_json = response.json().get('data', {}).get('data', None)
        if not secret_data_json:
            raise Exception(f'Failed to get secret data from Vault: {response.text}')
        
        return secret_data_json

def run():
    with open('config.yaml') as f:
        config = yaml.safe_load(f)

        vault_config = config.get('vault', {})
        output_file_path = config.get('output_file_path', 'output.json')
        refresh_interval_secs = config.get('refresh_interval_secs', 60)

        while True:
            vault = Vault(vault_config)
            vault.login()
            secret_data = vault.get_secret_data()

            with open(output_file_path, 'w') as f:
                f.write(json.dumps(secret_data, indent=2))
            time.sleep(refresh_interval_secs)

run()
