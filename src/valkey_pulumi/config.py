"""Configuration classes for Valkey deployment.

This module contains the main configuration classes used for Valkey deployment with Pulumi.
"""

import pulumi


def _coalesce(*values):
    """Return the first value that is not None."""
    for value in values:
        if value is not None:
            return value
    return None


# Default configuration structure matching Bitnami Valkey environment variables
DEFAULT_VALKEY_CONFIG = {
    # Basic Configuration
    "image": "docker.io/bitnami/valkey:9.0",
    "database": "valkey",
    "valkey_data_dir": "/bitnami/valkey/data",
    "valkey_overrides_file": None,  # Default: "${VALKEY_MOUNTED_CONF_DIR}/overrides.conf"
    "disable_commands": ("FLUSHDB", "FLUSHALL"),
    "extra_flags": (),
    # Persistence
    "aof_enabled": True,
    "rdb_policy": None,
    "rdb_policy_disabled": False,
    # Networking
    "primary_host": None,
    "primary_port_number": 6379,
    "port": 6379,
    "allow_remote_connections": True,
    # Replication
    "replication_mode": None,
    "replica_ip": None,
    "replica_port": None,
    "primary_password": None,
    # Authentication
    "password": None,
    "allow_empty_password": False,
    # Security
    "acl_file": None,
    # Performance
    "io_threads_do_reads": None,
    "io_threads": None,
    # TLS/SSL
    "tls_enabled": False,
    "tls_port_number": 6379,
    "tls_cert_file": None,
    "tls_key_file": None,
    "tls_ca_file": None,
    "tls_ca_dir": None,
    "tls_key_file_pass": None,
    "tls_dh_params_file": None,
    "tls_auth_clients": True,
    # Configuration Files
    "valkey_config_file": None,
    # Pulumi-specific deployment settings
    "persistence_enabled": True,
    "volume_name": None,
    "host_data_path": None,
    "restart_policy": "unless-stopped",
    "replica_count": 1,
    "replica_port_offset": 1,
    # Sentinel configuration
    "valkey_sentinel_primary_name": None,
    "valkey_sentinel_host": None,
    "valkey_sentinel_port_number": 26379,
    # For truly custom/unsupported environment variables
    "extra_env_vars": {},
}


class Config:
    """Configuration class for Valkey deployment."""

    def __init__(
        self,
        # Basic Configuration
        image: str | None = None,
        database: str | None = None,
        valkey_data_dir: str | None = None,
        valkey_overrides_file: str | None = None,
        disable_commands: list[str] | None = None,
        extra_flags: list[str] | None = None,
        # Persistence
        aof_enabled: bool | None = None,
        rdb_policy: str | None = None,
        rdb_policy_disabled: bool | None = None,
        # Networking
        primary_host: str | None = None,
        primary_port_number: int | None = None,
        port: int | None = None,
        allow_remote_connections: bool | None = None,
        # Replication
        replication_mode: str | None = None,
        replica_ip: str | None = None,
        replica_port: int | None = None,
        primary_password: str | None = None,
        # Authentication
        password: str | None = None,
        allow_empty_password: bool | None = None,
        # Security
        acl_file: str | None = None,
        # Performance
        io_threads_do_reads: bool | None = None,
        io_threads: int | None = None,
        # TLS/SSL
        tls_enabled: bool | None = None,
        tls_port_number: int | None = None,
        tls_cert_file: str | None = None,
        tls_key_file: str | None = None,
        tls_ca_file: str | None = None,
        tls_ca_dir: str | None = None,
        tls_key_file_pass: str | None = None,
        tls_dh_params_file: str | None = None,
        tls_auth_clients: bool | None = None,
        # Configuration Files
        valkey_config_file: str | None = None,
        # Pulumi-specific deployment settings
        persistence_enabled: bool | None = None,
        volume_name: str | None = None,
        host_data_path: str | None = None,
        restart_policy: str | None = None,
        replica_count: int | None = None,
        replica_port_offset: int | None = None,
        # Sentinel configuration
        valkey_sentinel_primary_name: str | None = None,
        valkey_sentinel_host: str | None = None,
        valkey_sentinel_port_number: int | None = None,
        # Custom environment variables
        extra_env_vars: dict[str, str] | None = None,
    ):
        pulumi_config = pulumi.Config()

        # Basic Configuration
        self.image = _coalesce(image, pulumi_config.get("valkey:image"), DEFAULT_VALKEY_CONFIG["image"])
        self.database = _coalesce(database, pulumi_config.get("valkey:database"), DEFAULT_VALKEY_CONFIG["database"])
        self.valkey_data_dir = _coalesce(
            valkey_data_dir, pulumi_config.get("valkey:valkey_data_dir"), DEFAULT_VALKEY_CONFIG["valkey_data_dir"]
        )
        self.valkey_overrides_file = _coalesce(
            valkey_overrides_file,
            pulumi_config.get("valkey:valkey_overrides_file"),
            DEFAULT_VALKEY_CONFIG["valkey_overrides_file"],
        )
        self.disable_commands = _coalesce(
            disable_commands,
            pulumi_config.get_object("valkey:disable_commands"),
            DEFAULT_VALKEY_CONFIG["disable_commands"],
        )
        self.extra_flags = tuple(
            _coalesce(extra_flags, pulumi_config.get_object("valkey:extra_flags"), DEFAULT_VALKEY_CONFIG["extra_flags"])
        )

        # Persistence
        self.aof_enabled = _coalesce(
            aof_enabled, pulumi_config.get_bool("valkey:aof_enabled"), DEFAULT_VALKEY_CONFIG["aof_enabled"]
        )
        self.rdb_policy = _coalesce(
            rdb_policy, pulumi_config.get("valkey:rdb_policy"), DEFAULT_VALKEY_CONFIG["rdb_policy"]
        )
        self.rdb_policy_disabled = _coalesce(
            rdb_policy_disabled,
            pulumi_config.get_bool("valkey:rdb_policy_disabled"),
            DEFAULT_VALKEY_CONFIG["rdb_policy_disabled"],
        )

        # Networking
        self.primary_host = _coalesce(
            primary_host, pulumi_config.get("valkey:primary_host"), DEFAULT_VALKEY_CONFIG["primary_host"]
        )
        self.primary_port_number = _coalesce(
            primary_port_number,
            pulumi_config.get_int("valkey:primary_port_number"),
            DEFAULT_VALKEY_CONFIG["primary_port_number"],
        )
        self.port = _coalesce(port, pulumi_config.get_int("valkey:port"), DEFAULT_VALKEY_CONFIG["port"])
        self.allow_remote_connections = _coalesce(
            allow_remote_connections,
            pulumi_config.get_bool("valkey:allow_remote_connections"),
            DEFAULT_VALKEY_CONFIG["allow_remote_connections"],
        )

        # Replication
        self.replication_mode = _coalesce(
            replication_mode, pulumi_config.get("valkey:replication_mode"), DEFAULT_VALKEY_CONFIG["replication_mode"]
        )
        self.replica_ip = _coalesce(
            replica_ip, pulumi_config.get("valkey:replica_ip"), DEFAULT_VALKEY_CONFIG["replica_ip"]
        )
        self.replica_port = _coalesce(
            replica_port, pulumi_config.get_int("valkey:replica_port"), DEFAULT_VALKEY_CONFIG["replica_port"]
        )
        self.primary_password = _coalesce(primary_password, pulumi_config.get_secret("valkey:primary_password"))

        # Authentication
        self.password = _coalesce(password, pulumi_config.get_secret("valkey:password"))
        self.allow_empty_password = _coalesce(
            allow_empty_password,
            pulumi_config.get_bool("valkey:allow_empty_password"),
            DEFAULT_VALKEY_CONFIG["allow_empty_password"],
        )

        # Security
        self.acl_file = _coalesce(acl_file, pulumi_config.get("valkey:acl_file"), DEFAULT_VALKEY_CONFIG["acl_file"])

        # Performance
        self.io_threads_do_reads = _coalesce(
            io_threads_do_reads,
            pulumi_config.get_bool("valkey:io_threads_do_reads"),
            DEFAULT_VALKEY_CONFIG["io_threads_do_reads"],
        )
        self.io_threads = _coalesce(
            io_threads, pulumi_config.get_int("valkey:io_threads"), DEFAULT_VALKEY_CONFIG["io_threads"]
        )

        # TLS/SSL
        self.tls_enabled = _coalesce(
            tls_enabled, pulumi_config.get_bool("valkey:tls_enabled"), DEFAULT_VALKEY_CONFIG["tls_enabled"]
        )
        self.tls_port_number = _coalesce(
            tls_port_number, pulumi_config.get_int("valkey:tls_port_number"), DEFAULT_VALKEY_CONFIG["tls_port_number"]
        )
        self.tls_cert_file = _coalesce(
            tls_cert_file, pulumi_config.get("valkey:tls_cert_file"), DEFAULT_VALKEY_CONFIG["tls_cert_file"]
        )
        self.tls_key_file = _coalesce(
            tls_key_file, pulumi_config.get("valkey:tls_key_file"), DEFAULT_VALKEY_CONFIG["tls_key_file"]
        )
        self.tls_ca_file = _coalesce(
            tls_ca_file, pulumi_config.get("valkey:tls_ca_file"), DEFAULT_VALKEY_CONFIG["tls_ca_file"]
        )
        self.tls_ca_dir = _coalesce(
            tls_ca_dir, pulumi_config.get("valkey:tls_ca_dir"), DEFAULT_VALKEY_CONFIG["tls_ca_dir"]
        )
        self.tls_key_file_pass = _coalesce(tls_key_file_pass, pulumi_config.get_secret("valkey:tls_key_file_pass"))
        self.tls_dh_params_file = _coalesce(
            tls_dh_params_file,
            pulumi_config.get("valkey:tls_dh_params_file"),
            DEFAULT_VALKEY_CONFIG["tls_dh_params_file"],
        )
        self.tls_auth_clients = _coalesce(
            tls_auth_clients,
            pulumi_config.get_bool("valkey:tls_auth_clients"),
            DEFAULT_VALKEY_CONFIG["tls_auth_clients"],
        )

        # Configuration Files
        self.valkey_config_file = _coalesce(
            valkey_config_file,
            pulumi_config.get("valkey:valkey_config_file"),
            DEFAULT_VALKEY_CONFIG["valkey_config_file"],
        )

        # Pulumi-specific deployment settings
        self.persistence_enabled = _coalesce(
            persistence_enabled,
            pulumi_config.get_bool("valkey:persistence_enabled"),
            DEFAULT_VALKEY_CONFIG["persistence_enabled"],
        )
        self.volume_name = _coalesce(
            volume_name, pulumi_config.get("valkey:volume_name"), DEFAULT_VALKEY_CONFIG["volume_name"]
        )
        self.host_data_path = _coalesce(
            host_data_path, pulumi_config.get("valkey:host_data_path"), DEFAULT_VALKEY_CONFIG["host_data_path"]
        )
        self.restart_policy = _coalesce(
            restart_policy, pulumi_config.get("valkey:restart_policy"), DEFAULT_VALKEY_CONFIG["restart_policy"]
        )
        self.replica_count = _coalesce(
            replica_count, pulumi_config.get_int("valkey:replica_count"), DEFAULT_VALKEY_CONFIG["replica_count"]
        )
        self.replica_port_offset = _coalesce(
            replica_port_offset,
            pulumi_config.get_int("valkey:replica_port_offset"),
            DEFAULT_VALKEY_CONFIG["replica_port_offset"],
        )

        # Sentinel configuration
        self.valkey_sentinel_primary_name = _coalesce(
            valkey_sentinel_primary_name,
            pulumi_config.get("valkey:valkey_sentinel_primary_name"),
            DEFAULT_VALKEY_CONFIG["valkey_sentinel_primary_name"],
        )
        self.valkey_sentinel_host = _coalesce(
            valkey_sentinel_host,
            pulumi_config.get("valkey:valkey_sentinel_host"),
            DEFAULT_VALKEY_CONFIG["valkey_sentinel_host"],
        )
        self.valkey_sentinel_port_number = _coalesce(
            valkey_sentinel_port_number,
            pulumi_config.get_int("valkey:valkey_sentinel_port_number"),
            DEFAULT_VALKEY_CONFIG["valkey_sentinel_port_number"],
        )

        # Extra environment variables (truly custom ones)
        config_extra_env_vars = (
            pulumi_config.get_object("valkey:extra_env_vars") or DEFAULT_VALKEY_CONFIG["extra_env_vars"]
        )
        self.extra_env_vars = extra_env_vars or config_extra_env_vars
