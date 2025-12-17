"""Pulumi Python code for deploying Valkey using Docker backend.

This module provides Valkey deployment configurations compatible with
Bitnami's Valkey Docker images and Docker Compose configurations.
"""

import os
from typing import Any

import pulumi
import pulumi_docker as docker

from .config import Config

CONFIG_MOUNT_PATH = "/opt/bitnami/valkey/mounted-etc/valkey.conf"
OVERRIDES_MOUNT_PATH = "/opt/bitnami/valkey/mounted-etc/overrides.conf"
ACL_MOUNT_PATH = "/opt/bitnami/valkey/mounted-etc/users.acl"


def _bool_to_yes_no(value: bool | None) -> str | None:
    if value is None:
        return None
    return "yes" if value else "no"


def _env_args(env_map: dict[str, str | None]) -> list[str]:
    """Convert a mapping of env var names to Pulumi container env args."""
    args: list[str] = []
    for name, value in env_map.items():
        if value is None:
            continue
        args.append(f"{name}={value}")
    return args


def _build_env(config: Config, overrides: dict[str, str | None] | None = None) -> list[str]:
    """Build environment variables for a container from a Config."""
    env_map: dict[str, str | None] = {
        # Authentication
        "ALLOW_EMPTY_PASSWORD": "yes" if config.allow_empty_password else None,
        "VALKEY_PASSWORD": config.password,
        "VALKEY_PRIMARY_PASSWORD": config.primary_password,
        # Core configuration
        "VALKEY_DISABLE_COMMANDS": ",".join(config.disable_commands) if config.disable_commands else None,
        "VALKEY_DATA_DIR": config.valkey_data_dir,
        "VALKEY_DATABASE": config.database,
        "VALKEY_OVERRIDES_FILE": OVERRIDES_MOUNT_PATH if config.valkey_overrides_file else None,
        "VALKEY_AOF_ENABLED": _bool_to_yes_no(config.aof_enabled),
        "VALKEY_RDB_POLICY": config.rdb_policy,
        "VALKEY_RDB_POLICY_DISABLED": _bool_to_yes_no(config.rdb_policy_disabled),
        "VALKEY_EXTRA_FLAGS": " ".join(config.extra_flags) if config.extra_flags else None,
        # Networking
        "VALKEY_PRIMARY_HOST": config.primary_host,
        "VALKEY_PRIMARY_PORT_NUMBER": str(config.primary_port_number)
        if config.primary_port_number is not None
        else None,
        "VALKEY_PORT_NUMBER": str(config.port) if config.port is not None else None,
        "VALKEY_ALLOW_REMOTE_CONNECTIONS": _bool_to_yes_no(config.allow_remote_connections),
        # Replication
        "VALKEY_REPLICATION_MODE": config.replication_mode,
        "VALKEY_REPLICA_IP": config.replica_ip,
        "VALKEY_REPLICA_PORT": str(config.replica_port) if config.replica_port is not None else None,
        # Security
        "VALKEY_ACLFILE": ACL_MOUNT_PATH if config.acl_file else None,
        # Performance
        "VALKEY_IO_THREADS_DO_READS": _bool_to_yes_no(config.io_threads_do_reads),
        "VALKEY_IO_THREADS": str(config.io_threads) if config.io_threads is not None else None,
        # TLS/SSL
        "VALKEY_TLS_ENABLED": _bool_to_yes_no(config.tls_enabled),
        "VALKEY_TLS_PORT_NUMBER": str(config.tls_port_number) if config.tls_port_number is not None else None,
        "VALKEY_TLS_CERT_FILE": os.path.abspath(config.tls_cert_file) if config.tls_cert_file else None,
        "VALKEY_TLS_KEY_FILE": os.path.abspath(config.tls_key_file) if config.tls_key_file else None,
        "VALKEY_TLS_CA_FILE": os.path.abspath(config.tls_ca_file) if config.tls_ca_file else None,
        "VALKEY_TLS_CA_DIR": os.path.abspath(config.tls_ca_dir) if config.tls_ca_dir else None,
        "VALKEY_TLS_KEY_FILE_PASS": config.tls_key_file_pass,
        "VALKEY_TLS_DH_PARAMS_FILE": os.path.abspath(config.tls_dh_params_file) if config.tls_dh_params_file else None,
        "VALKEY_TLS_AUTH_CLIENTS": _bool_to_yes_no(config.tls_auth_clients),
        # Sentinel
        "VALKEY_SENTINEL_PRIMARY_NAME": config.valkey_sentinel_primary_name,
        "VALKEY_SENTINEL_HOST": config.valkey_sentinel_host,
        "VALKEY_SENTINEL_PORT_NUMBER": str(config.valkey_sentinel_port_number)
        if config.valkey_sentinel_port_number is not None
        else None,
    }

    if overrides:
        env_map.update(overrides)

    env_vars = _env_args(env_map)

    # Extra environment variables (truly custom ones)
    for key, value in config.extra_env_vars.items():
        env_vars.append(f"{key}={value}")

    return env_vars


def _file_mounts(config: Config) -> list[docker.ContainerVolumeArgs]:
    """Create file/directory mounts (TLS, ACL, config) for a container."""
    mounts: list[docker.ContainerVolumeArgs] = []

    if config.tls_cert_file:
        mounts.append(
            docker.ContainerVolumeArgs(
                container_path=os.path.abspath(config.tls_cert_file),
                host_path=os.path.abspath(config.tls_cert_file),
                volume_name=None,
                read_only=True,
            )
        )
    if config.tls_key_file:
        mounts.append(
            docker.ContainerVolumeArgs(
                container_path=os.path.abspath(config.tls_key_file),
                host_path=os.path.abspath(config.tls_key_file),
                volume_name=None,
                read_only=True,
            )
        )
    if config.tls_ca_file:
        mounts.append(
            docker.ContainerVolumeArgs(
                container_path=os.path.abspath(config.tls_ca_file),
                host_path=os.path.abspath(config.tls_ca_file),
                volume_name=None,
                read_only=True,
            )
        )
    if config.tls_dh_params_file:
        mounts.append(
            docker.ContainerVolumeArgs(
                container_path=os.path.abspath(config.tls_dh_params_file),
                host_path=os.path.abspath(config.tls_dh_params_file),
                volume_name=None,
                read_only=True,
            )
        )
    if config.tls_ca_dir:
        mounts.append(
            docker.ContainerVolumeArgs(
                container_path=os.path.abspath(config.tls_ca_dir),
                host_path=os.path.abspath(config.tls_ca_dir),
                volume_name=None,
                read_only=True,
            )
        )

    if config.acl_file:
        mounts.append(
            docker.ContainerVolumeArgs(
                container_path=ACL_MOUNT_PATH,
                host_path=os.path.abspath(config.acl_file),
                volume_name=None,
                read_only=True,
            )
        )

    if config.valkey_config_file:
        mounts.append(
            docker.ContainerVolumeArgs(
                container_path=CONFIG_MOUNT_PATH,
                host_path=os.path.abspath(config.valkey_config_file),
                volume_name=None,
                read_only=True,
            )
        )

    if config.valkey_overrides_file:
        mounts.append(
            docker.ContainerVolumeArgs(
                container_path=OVERRIDES_MOUNT_PATH,
                host_path=os.path.abspath(config.valkey_overrides_file),
                volume_name=None,
                read_only=True,
            )
        )

    return mounts


class ValkeyStandalone:
    """Standalone Valkey deployment using Docker."""

    def __init__(self, name: str, config: Config):
        self.name = name
        self.config = config
        self._deploy()

    def _deploy(self):
        """Deploy the standalone Valkey container."""
        volume_name = self.config.volume_name or f"{self.name}_data"

        # Create volume/bind for data persistence
        volumes: list[docker.ContainerVolumeArgs] = []
        if self.config.host_data_path:
            volumes.append(
                docker.ContainerVolumeArgs(
                    container_path=self.config.valkey_data_dir,
                    host_path=os.path.abspath(self.config.host_data_path),
                    volume_name=None,
                    read_only=False,
                )
            )
        elif self.config.persistence_enabled:
            self.volume = docker.Volume(volume_name, name=volume_name, driver="local")
            volumes.append(
                docker.ContainerVolumeArgs(
                    container_path=self.config.valkey_data_dir,
                    volume_name=self.volume.name,
                    host_path=None,
                    read_only=False,
                )
            )

        # Add mounts for TLS, ACL, and config files
        volumes.extend(_file_mounts(self.config))

        # Create Valkey container
        depends_on = []
        if self.config.persistence_enabled and not self.config.host_data_path:
            depends_on.append(self.volume)

        self.container = docker.Container(
            self.name,
            name=self.name,
            image=docker.RemoteImage(f"{self.name}_image", name=self.config.image, keep_locally=False),
            ports=[docker.ContainerPortArgs(internal=self.config.port, external=self.config.port)],
            envs=_build_env(self.config),
            restart=self.config.restart_policy,
            volumes=volumes,
            opts=pulumi.ResourceOptions(depends_on=depends_on if depends_on else None),
        )

        # Export connection details
        pulumi.export(f"{self.name}_host", self.container.name)
        pulumi.export(f"{self.name}_port", self.config.port)
        pulumi.export(f"{self.name}_endpoint", self.container.name.apply(lambda name: f"{name}:{self.config.port}"))


class ValkeyReplicaSet:
    """Valkey primary-replica deployment using Docker."""

    def __init__(
        self,
        name: str,
        primary_config: Config,
        replica_config: Config,
        replica_count: int | None = None,
        replica_port_offset: int | None = None,
    ):
        self.name = name
        self.primary_config = primary_config
        self.replica_config = replica_config
        self.replica_count = replica_count if replica_count is not None else self.replica_config.replica_count
        self.replica_port_offset = (
            replica_port_offset if replica_port_offset is not None else self.replica_config.replica_port_offset
        )
        self._deploy()

    def _get_primary_environment(self) -> list[str]:
        """Build environment variables for primary container."""
        overrides = {"VALKEY_REPLICATION_MODE": "primary"}
        return _build_env(self.primary_config, overrides)

    def _get_replica_environment(self) -> list[str]:
        """Build environment variables for replica containers."""
        primary_password = self.primary_config.password or self.replica_config.password

        overrides = {
            "VALKEY_REPLICATION_MODE": "replica",
            "VALKEY_PRIMARY_HOST": f"{self.name}-primary",
            "VALKEY_PRIMARY_PORT_NUMBER": str(self.primary_config.port),
            "VALKEY_PRIMARY_PASSWORD": primary_password,
            "VALKEY_PASSWORD": primary_password,
        }

        if not primary_password and self.replica_config.allow_empty_password:
            overrides["ALLOW_EMPTY_PASSWORD"] = "yes"

        return _build_env(self.replica_config, overrides)

    def _deploy(self):
        """Deploy the Valkey replica set."""
        # Create shared network for communication
        self.network = docker.Network(f"{self.name}_network", name=f"{self.name}_network", driver="bridge")

        # Deploy primary container
        primary_volumes = _file_mounts(self.primary_config)
        primary_depends: list[pulumi.Resource] = [self.network]
        if self.primary_config.host_data_path:
            primary_volumes.append(
                docker.ContainerVolumeArgs(
                    container_path=self.primary_config.valkey_data_dir,
                    host_path=os.path.abspath(self.primary_config.host_data_path),
                    volume_name=None,
                    read_only=False,
                )
            )
        elif self.primary_config.persistence_enabled:
            volume_name = self.primary_config.volume_name or f"{self.name}_primary_data"
            self.primary_volume = docker.Volume(volume_name, name=volume_name, driver="local")
            primary_depends.append(self.primary_volume)
            primary_volumes.append(
                docker.ContainerVolumeArgs(
                    container_path=self.primary_config.valkey_data_dir,
                    volume_name=self.primary_volume.name,
                    host_path=None,
                    read_only=False,
                )
            )

        self.primary = docker.Container(
            f"{self.name}-primary",
            name=f"{self.name}-primary",
            image=docker.RemoteImage(f"{self.name}_primary_image", name=self.primary_config.image, keep_locally=False),
            ports=[docker.ContainerPortArgs(internal=self.primary_config.port, external=self.primary_config.port)],
            envs=self._get_primary_environment(),
            restart=self.primary_config.restart_policy,
            volumes=primary_volumes,
            networks_advanced=[
                docker.ContainerNetworksAdvancedArgs(name=self.network.name, aliases=[f"{self.name}-primary"])
            ],
            opts=pulumi.ResourceOptions(depends_on=primary_depends),
        )

        # Deploy replica containers
        self.replicas = []
        self.replica_volumes: list[docker.Volume] = []
        for i in range(self.replica_count):
            replica_name = f"{self.name}-replica-{i}"

            replica_volumes = _file_mounts(self.replica_config)
            replica_depends_on: list[pulumi.Resource] = [self.network, self.primary]

            if self.replica_config.host_data_path:
                replica_volumes.append(
                    docker.ContainerVolumeArgs(
                        container_path=self.replica_config.valkey_data_dir,
                        host_path=os.path.abspath(self.replica_config.host_data_path),
                        volume_name=None,
                        read_only=False,
                    )
                )
            elif self.replica_config.persistence_enabled:
                replica_volume = docker.Volume(f"{replica_name}_data", name=f"{replica_name}_data", driver="local")
                self.replica_volumes.append(replica_volume)
                replica_volumes.append(
                    docker.ContainerVolumeArgs(
                        container_path=self.replica_config.valkey_data_dir,
                        volume_name=replica_volume.name,
                        host_path=None,
                        read_only=False,
                    )
                )
                replica_depends_on.append(replica_volume)

            replica = docker.Container(
                replica_name,
                name=replica_name,
                image=docker.RemoteImage(f"{replica_name}_image", name=self.replica_config.image, keep_locally=False),
                ports=[
                    docker.ContainerPortArgs(
                        internal=self.replica_config.port,
                        external=self.replica_config.port
                        + self.replica_port_offset
                        + i,  # Use different external ports with configurable offset
                    )
                ],
                envs=self._get_replica_environment(),
                restart=self.replica_config.restart_policy,
                volumes=replica_volumes,
                networks_advanced=[
                    docker.ContainerNetworksAdvancedArgs(name=self.network.name, aliases=[replica_name])
                ],
                opts=pulumi.ResourceOptions(depends_on=replica_depends_on),
            )
            self.replicas.append(replica)

        # Export connection details
        pulumi.export(f"{self.name}_primary_host", self.primary.name)
        pulumi.export(f"{self.name}_primary_port", self.primary_config.port)
        pulumi.export(
            f"{self.name}_primary_endpoint", self.primary.name.apply(lambda name: f"{name}:{self.primary_config.port}")
        )

        replica_endpoints = []
        for i, replica in enumerate(self.replicas):
            replica_external_port = self.replica_config.port + self.replica_port_offset + i
            pulumi.export(f"{self.name}_replica_{i}_host", replica.name)
            pulumi.export(f"{self.name}_replica_{i}_port", replica_external_port)
            replica_endpoints.append(replica.name.apply(lambda name, port=replica_external_port: f"{name}:{port}"))

        pulumi.export(f"{self.name}_replica_endpoints", replica_endpoints)


def create_standalone_valkey(name: str, **kwargs) -> ValkeyStandalone:
    """Helper function to create a standalone Valkey deployment.

    Args:
        name: Name of the Valkey deployment
        **kwargs: Configuration options for Config

    Returns:
        ValkeyStandalone instance

    """
    config = Config(**kwargs)
    return ValkeyStandalone(name, config)


def create_valkey_replica_set(
    name: str,
    replica_count: int | None = None,
    replica_port_offset: int | None = None,
    primary_config: dict[str, Any] | None = None,
    replica_config: dict[str, Any] | None = None,
) -> ValkeyReplicaSet:
    """Helper function to create a Valkey replica set deployment.

    Args:
        name: Name of the Valkey replica set
        replica_count: Number of replica containers (optional, reads from config)
        replica_port_offset: Port offset for replicas (optional, reads from config)
        primary_config: Configuration dict for primary
        replica_config: Configuration dict for replicas

    Returns:
        ValkeyReplicaSet instance

    """
    primary_kwargs = primary_config or {}
    replica_kwargs = replica_config or {}

    # Ensure passwords are synchronized if not explicitly set
    if "password" not in primary_kwargs and "password" in replica_kwargs:
        primary_kwargs["password"] = replica_kwargs["password"]

    primary_config = Config(**primary_kwargs)
    replica_config = Config(**replica_kwargs)

    return ValkeyReplicaSet(name, primary_config, replica_config, replica_count, replica_port_offset)


# Example usage
if __name__ == "__main__":
    # Example 1: Standalone Valkey with authentication
    standalone_config = {
        "password": "my_secure_password",
        "disable_commands": ["FLUSHDB", "FLUSHALL"],
        "persistence_enabled": True,
    }

    valkey_standalone = create_standalone_valkey("my-valkey", **standalone_config)

    # Example 2: Valkey replica set
    primary_config = {
        "password": "my_replica_password",
        "disable_commands": ["FLUSHDB", "FLUSHALL"],
        "persistence_enabled": True,
    }

    replica_config = {"disable_commands": ["FLUSHDB", "FLUSHALL"]}

    valkey_replica_set = create_valkey_replica_set(
        "my-valkey-replica-set", replica_count=2, primary_config=primary_config, replica_config=replica_config
    )
