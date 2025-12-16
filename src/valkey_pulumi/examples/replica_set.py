"""Example: Deploy Valkey primary-replica set using Pulumi.

This example demonstrates how to deploy a Valkey replica set with one primary
and multiple replica containers, compatible with Bitnami's Valkey Docker Compose
replica set configuration.
"""

import os
import sys

# Add the parent directory to the path to import the valkey module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from valkey_pulumi import create_valkey_replica_set


def deploy_valkey_replica_set():
    """Deploy a Valkey replica set using Pulumi configuration.

    This deployment reads configuration from Pulumi.dev.yaml (or current stack config).
    """
    # Deploy replica set using configuration from Pulumi config
    # All values will be read from Pulumi.dev.yaml unless explicitly provided
    replica_set = create_valkey_replica_set("valkey-replica-set")

    return replica_set


def deploy_valkey_replica_set_with_overrides():
    """Deploy a Valkey replica set with configuration overrides.

    This shows how to override specific Pulumi configuration values.
    """
    # Override specific configuration values (others come from Pulumi config)
    primary_config = {
        "password": "my_password",  # Override config file password
        "volume_name": "valkey_replica_data",  # Override config file volume name
    }

    replica_config = {
        "password": "my_password",  # Use same password for replicas
    }

    # Deploy replica set with 2 replicas and overrides
    replica_set = create_valkey_replica_set(
        "valkey-replica-set-custom", replica_count=2, primary_config=primary_config, replica_config=replica_config
    )

    return replica_set


def deploy_simple_replica_set():
    """Deploy a simple Valkey replica set without authentication."""
    primary_config = {
        "image": "docker.io/bitnami/valkey:9.0",
        "allow_empty_password": True,
        "disable_commands": ["FLUSHDB", "FLUSHALL"],
        "port": 6379,
        "persistence_enabled": True,
        "replication_mode": "primary",
    }

    replica_config = {
        "allow_empty_password": True,
        "replication_mode": "replica",
    }

    replica_set = create_valkey_replica_set(
        "simple-valkey-replica",
        replica_count=1,
        primary_config=primary_config,
        replica_config=replica_config,
    )

    return replica_set


if __name__ == "__main__":
    # Deploy the Valkey replica set
    replica_set_instance = deploy_valkey_replica_set()

    print("Valkey replica set deployment created successfully!")
    print("Primary details:")
    print(f"  Host: {replica_set_instance.primary.name}")
    print("  Port: 6379")
    print("  Password: my_password")
    print(f"  Endpoint: {replica_set_instance.primary.name}:6379")

    print("\nReplica details:")
    for i, replica in enumerate(replica_set_instance.replicas):
        print(f"  Replica {i}:")
        print(f"    Host: {replica.name}")
        print(f"    Port: {6379 + i + 1}")
        print(f"    Endpoint: {replica.name}:{6379 + i + 1}")
