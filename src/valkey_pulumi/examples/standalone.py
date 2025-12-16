"""Example: Deploy a standalone Valkey instance using Pulumi.

This example demonstrates how to deploy a single Valkey container
with authentication and data persistence, compatible with Bitnami's
Valkey Docker Compose configuration.
"""

import os
import sys

# Add the parent directory to the path to import the valkey module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from valkey_pulumi import create_standalone_valkey


def deploy_standalone_valkey():
    """Deploy a standalone Valkey instance using Pulumi configuration.

    This deployment reads configuration from Pulumi.dev.yaml (or current stack config)
    and can be overridden by passing parameters.
    """
    # Deploy standalone Valkey with configuration from Pulumi config
    # These values will be read from Pulumi.dev.yaml unless explicitly provided here
    valkey = create_standalone_valkey("standalone-valkey")

    return valkey


def deploy_standalone_valkey_with_override():
    """Deploy a standalone Valkey instance with explicit configuration overrides.

    This shows how to override specific Pulumi configuration values.
    """
    # Override specific configuration values (others come from Pulumi config)
    config = {
        "password": "my_secure_password",  # Override config file password
        "volume_name": "my_valkey_data",  # Override config file volume name
    }

    # Deploy standalone Valkey with overrides
    valkey = create_standalone_valkey("standalone-valkey-custom", **config)

    return valkey


# Alternative deployment using helper function
def deploy_simple_valkey():
    """Deploy a simple Valkey instance without authentication (for development)."""
    valkey = create_standalone_valkey(
        "simple-valkey", allow_empty_password=True, disable_commands=["FLUSHDB", "FLUSHALL"], persistence_enabled=True
    )

    return valkey


if __name__ == "__main__":
    # Deploy the standalone Valkey instance
    valkey_instance = deploy_standalone_valkey()

    print("Standalone Valkey deployment created successfully!")
    print("Connection details:")
    print(f"  Host: {valkey_instance.container.name}")
    print("  Port: 6379")
    print("  Password: my_secure_password")
    print(f"  Endpoint: {valkey_instance.container.name}:6379")
