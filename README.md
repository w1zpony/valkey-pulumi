# valkey-pulumi

[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

A Pulumi component for deploying Valkey (Redis-compatible in-memory data structure store) with Docker.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Pulumi CLI](https://www.pulumi.com/docs/get-started/install/)
- [Docker](https://www.docker.com/get-started/)
- Recommended: [mise](https://mise.dev/) for environment management

### Installation

```bash
# Clone the repository
git clone https://github.com/daotl/valkey-pulumi.git
cd valkey-pulumi

# Install dependencies and set up environment
mise install
```

### Basic Usage

1. **Create a basic Valkey deployment:**

```python
# __main__.py
from valkey_pulumi import create_standalone_valkey

# Simple deployment with default configuration
valkey = create_standalone_valkey("my-valkey")
```

2. **Deploy with Pulumi:**

```bash
pulumi stack init dev
pulumi up
```

3. **Connect to your Valkey:**

```bash
# Get connection details
pulumi stack output

# Connect with redis-cli
redis-cli -h $(pulumi stack output -j | jq -r '.my_valkey_host') \
         -p $(pulumi stack output -j | jq -r '.my_valkey_port')
```

## 📖 Configuration

### Configuration Structure

Valkey deployments are configured using `Pulumi.<stack>.yaml` files. The configuration supports all [Bitnami Valkey environment variables](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#configuration) and features. See the complete [Bitnami Valkey documentation](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md) for detailed information about:

- [Configuration parameters](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#configuration)
- [Persistence and AOF settings](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#persistence)
- [Security and authentication](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#security)
- [Replication configuration](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#replication)
- [Logging configuration](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#logging)
- [TLS/SSL support](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#securing-traffic-using-tls)

### Environment Variable Mapping

Our Pulumi configuration uses clean, readable parameter names that map to Bitnami Valkey environment variables. The following table shows all customizable environment variables from the Bitnami Valkey container:

**Customizable Environment Variables:**

The following configuration options are supported directly by Bitnami Valkey environment variables:

**Important Note**: For Valkey configuration directives not available as environment variables (such as `appendfsync`, `client-output-buffer-limit`, `tcp-keepalive`, etc.), provide a custom configuration file using the `valkey_config_file` parameter. See the [Advanced Configuration](#advanced-configuration) section below for details.

| Pulumi Config | Implementation | Default Value | Description |
|---------------|-------------|---------------|-------------|
| **Basic Configuration** | | | |
| `valkey_data_dir` | `VALKEY_DATA_DIR` | `/bitnami/valkey/data` | Valkey data directory |
| `valkey_overrides_file` | `VALKEY_OVERRIDES_FILE` | `${VALKEY_MOUNTED_CONF_DIR}/overrides.conf` | Valkey config overrides file |
| `disable_commands` | `VALKEY_DISABLE_COMMANDS` | `nil` | Commands to disable in Valkey |
| `database` | `VALKEY_DATABASE` | `valkey` | Default Valkey database |
| **Persistence** | | | |
| `aof_enabled` | `VALKEY_AOF_ENABLED` | `yes` | Enable AOF |
| `rdb_policy` | `VALKEY_RDB_POLICY` | `nil` | Enable RDB policy persistence |
| `rdb_policy_disabled` | `VALKEY_RDB_POLICY_DISABLED` | `no` | Allows to enable RDB policy persistence |
| **Networking** | | | |
| `primary_host` | `VALKEY_PRIMARY_HOST` | `nil` | Valkey primary host (used by replicas) |
| `primary_port_number` | `VALKEY_PRIMARY_PORT_NUMBER` | `6379` | Valkey primary host port (used by replicas) |
| `port` | `VALKEY_PORT_NUMBER` | `$VALKEY_DEFAULT_PORT_NUMBER` | Valkey port number |
| `allow_remote_connections` | `VALKEY_ALLOW_REMOTE_CONNECTIONS` | `yes` | Allow remote connection to the service |
| **Replication** | | | |
| `replication_mode` | `VALKEY_REPLICATION_MODE` | `nil` | Valkey replication mode (values: primary, replica) |
| `replica_ip` | `VALKEY_REPLICA_IP` | `nil` | The replication announce ip |
| `replica_port` | `VALKEY_REPLICA_PORT` | `nil` | The replication announce port |
| **Authentication** | | | |
| `allow_empty_password` | `ALLOW_EMPTY_PASSWORD` | `no` | Allow password-less access |
| `password` | `VALKEY_PASSWORD` | `nil` | Password for Valkey |
| `primary_password` | `VALKEY_PRIMARY_PASSWORD` | `nil` | Valkey primary node password |
| **Security** | | | |
| `acl_file` | `VALKEY_ACLFILE` | `nil` | Valkey ACL file |
| **Performance** | | | |
| `io_threads_do_reads` | `VALKEY_IO_THREADS_DO_READS` | `nil` | Enable multithreading when reading socket |
| `io_threads` | `VALKEY_IO_THREADS` | `nil` | Number of threads |
| `extra_flags` | `VALKEY_EXTRA_FLAGS` | `nil` | Additional flags pass to 'valkey-server' commands |
| **TLS/SSL** | | | |
| `tls_enabled` | `VALKEY_TLS_ENABLED` | `no` | Enable TLS |
| `tls_port_number` | `VALKEY_TLS_PORT_NUMBER` | `6379` | Valkey TLS port (requires VALKEY_ENABLE_TLS=yes) |
| `tls_cert_file` | `VALKEY_TLS_CERT_FILE` | `nil` | Valkey TLS certificate file |
| `tls_ca_dir` | `VALKEY_TLS_CA_DIR` | `nil` | Directory containing TLS CA certificates |
| `tls_key_file` | `VALKEY_TLS_KEY_FILE` | `nil` | Valkey TLS key file |
| `tls_key_file_pass` | `VALKEY_TLS_KEY_FILE_PASS` | `nil` | Valkey TLS key file passphrase |
| `tls_ca_file` | `VALKEY_TLS_CA_FILE` | `nil` | Valkey TLS CA file |
| `tls_dh_params_file` | `VALKEY_TLS_DH_PARAMS_FILE` | `nil` | Valkey TLS DH parameter file |
| `tls_auth_clients` | `VALKEY_TLS_AUTH_CLIENTS` | `yes` | Enable Valkey TLS client authentication |
| **Configuration Files** | | | |
| `valkey_config_file` | Custom config file path | - | Path to custom Valkey configuration file for advanced settings |
| **Sentinel** | | | |
| `valkey_sentinel_primary_name` | `VALKEY_SENTINEL_PRIMARY_NAME` | `nil` | Valkey Sentinel primary name |
| `valkey_sentinel_host` | `VALKEY_SENTINEL_HOST` | `nil` | Valkey Sentinel host |
| `valkey_sentinel_port_number` | `VALKEY_SENTINEL_PORT_NUMBER` | `26379` | Valkey Sentinel host port (used by replicas) |

**Pulumi-only Settings:**

These control how the Pulumi component provisions Docker resources and do not map to Bitnami environment variables.

| Pulumi Config | Default Value | Description |
|---------------|---------------|-------------|
| `persistence_enabled` | `true` | Whether to create and mount a Docker volume for data durability |
| `volume_name` | `null` | Optional explicit name for the Docker volume (auto-generated when omitted) |
| `host_data_path` | `null` | Bind-mount a host directory to the Valkey data dir (skips creating a Docker volume when set) |
| `restart_policy` | `"unless-stopped"` | Docker container restart policy |
| `replica_count` | `1` | Number of replicas to deploy (replica set helper only) |
| `replica_port_offset` | `1` | Offset added to external ports for replicas (replica set helper only) |

### Advanced Configuration with Custom Config Files

For Valkey configuration directives that are not available as environment variables, provide a custom configuration file using the `valkey_config_file` parameter:

**Common Advanced Settings:**
- `appendfsync` - AOF fsync policy (`always`, `everysec`, `no`)
- `maxmemory` - Maximum memory limit (e.g., `2gb`)
- `maxmemory-policy` - Memory eviction policy (e.g., `allkeys-lru`)
- `timeout` - Client timeout in seconds
- `tcp-keepalive` - TCP keepalive in seconds
- `protected-mode` - Enable/disable protected mode
- `loglevel` - Valkey log level (`debug`, `verbose`, `notice`, `warning`)
- `databases` - Number of databases
- `client-output-buffer-limit` - Client buffer limits
- `tcp-keepalive` - TCP keepalive settings

**Example Setup:**

```yaml
# Pulumi.dev.yaml
config:
  valkey:
    # Standard settings via environment variables
    aof_enabled: true
    database: "valkey"
    disable_commands: ["FLUSHDB", "FLUSHALL"]

    # Advanced settings via custom config file
    valkey_config_file: "./config/valkey-advanced.conf"
```

```bash
# Create custom configuration file
mkdir -p config
cat > config/valkey-advanced.conf << EOF
# Advanced Valkey Configuration
appendfsync everysec
maxmemory 2gb
maxmemory-policy allkeys-lru
timeout 300
tcp-keepalive 60
protected-mode yes
loglevel notice
databases 16

# Client buffer limits
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
EOF
```

**Production Example:**

```bash
cat > config/valkey-production.conf << EOF
# Production Valkey Configuration
appendfsync everysec
maxmemory 4gb
maxmemory-policy allkeys-lru
timeout 300
tcp-keepalive 60
protected-mode yes
loglevel notice
databases 16

# Production client buffer limits
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 512mb 128mb 120
client-output-buffer-limit pubsub 64mb 16mb 120
EOF
```

> **Note**: The custom configuration file is mounted to `/opt/bitnami/valkey/mounted-etc/valkey.conf` in the container. If you provide this file, the Bitnami overrides file (`valkey_overrides_file`) is ignored—use one or the other. Keep your custom config aligned with any environment-variable-driven settings you still want applied.

**Read-Only Environment Variables:**

These variables provide path information and are used internally by the Bitnami container:

| Variable | Value | Description |
|----------|-------|-------------|
| `VALKEY_VOLUME_DIR` | `/bitnami/valkey` | Persistence base directory |
| `VALKEY_BASE_DIR` | `${BITNAMI_ROOT_DIR}/valkey` | Valkey installation directory |
| `VALKEY_CONF_DIR` | `${VALKEY_BASE_DIR}/etc` | Valkey configuration directory |
| `VALKEY_DEFAULT_CONF_DIR` | `${VALKEY_BASE_DIR}/etc.default` | Valkey default configuration directory |
| `VALKEY_MOUNTED_CONF_DIR` | `${VALKEY_BASE_DIR}/mounted-etc` | Valkey mounted configuration directory |
| `VALKEY_CONF_FILE` | `${VALKEY_CONF_DIR}/valkey.conf` | Valkey configuration file |
| `VALKEY_LOG_DIR` | `${VALKEY_BASE_DIR}/logs` | Valkey logs directory |
| `VALKEY_LOG_FILE` | `${VALKEY_LOG_DIR}/valkey.log` | Valkey log file |
| `VALKEY_TMP_DIR` | `${VALKEY_BASE_DIR}/tmp` | Valkey temporary directory |
| `VALKEY_PID_FILE` | `${VALKEY_TMP_DIR}/valkey.pid` | Valkey PID file |
| `VALKEY_BIN_DIR` | `${VALKEY_BASE_DIR}/bin` | Valkey executables directory |
| `VALKEY_DAEMON_USER` | `valkey` | Valkey system user |
| `VALKEY_DAEMON_GROUP` | `valkey` | Valkey system group |
| `VALKEY_DEFAULT_PORT_NUMBER` | `6379` | Valkey port number (Build time) |


> **Note:** For the complete list of supported Bitnami Valkey environment variables, refer to the official [Bitnami Valkey Docker Hub page](https://hub.docker.com/r/bitnami/valkey).

```yaml
config:
  valkey:
    # Basic settings
    image: "docker.io/bitnami/valkey:9.0"
    port: 6379
    password: ""  # Set with: pulumi config set --secret valkey:password "your_password"
    allow_empty_password: false

    # Core Valkey configuration
    aof_enabled: true
    aof_fsync_policy: "everysec"  # always, everysec, no
    maxmemory: null               # e.g., "2gb" for memory limit
    maxmemory_policy: "allkeys-lru"
    databases: 16
    timeout: 300
    tcp_keepalive: 60
    protected_mode: true

    # Security
    disable_commands:
      - "FLUSHDB"
      - "FLUSHALL"

    # Persistence and scaling
    persistence_enabled: true
    replica_count: 1

    # Advanced features (uncomment as needed)
    # tls_enabled: true
    # tls_cert_file: "/path/to/cert.pem"
    # tls_key_file: "/path/to/key.pem"
    # acl_file: "/path/to/acl.conf"

    # Use a host bind mount instead of a Docker volume
    # host_data_path: "/srv/valkey-data"
    # valkey_data_dir: "/bitnami/valkey/data"  # optional override of container path
```

### Setting Configuration

```bash
# Set password securely
pulumi config set --secret valkey:password "your_secure_password"

# Set configuration values
pulumi config set valkey:maxmemory "2gb"
pulumi config set valkey:replica_count 3
pulumi config set valkey:aof_fsync_policy "always"

# Enable security features
pulumi config set valkey:tls_enabled true
pulumi config set valkey:tls_cert_file "/path/to/cert.pem"
```

## 🔧 Deployment Examples

### Running Examples

The project includes several ready-to-run examples demonstrating different configurations (Standalone, Replica Set, ACL, TLS).

1.  **Configure Pulumi to run examples:**
    Change work directory to `src/valkey_pulumi/examples`, change `Pulumi.yaml` to point to the examples entry point:
    ```yaml
    main: ./__main__.py # acl_example.py,replica_set.py,standalone.py,tls_example.py
    ```
    The default value for the `main` parameter is the `__main__.py` in the current directory.

2.  **Run a specific example using the `VALKEY_EXAMPLE` environment variable:**

    *   **Standalone (Default):**
        ```bash
        pulumi up
        ```

    *   **Replica Set:**
        ```bash
        VALKEY_EXAMPLE=replica_set pulumi up
        ```

    *   **Access Control List (ACL):**
        ```bash
        VALKEY_EXAMPLE=acl pulumi up
        ```

    *   **TLS Encryption:**
        *(Requires valid certificates in `/etc/ssl/certs` and `/etc/ssl/private`)*
        ```bash
        VALKEY_EXAMPLE=tls pulumi up
        ```

    > **Note:** When switching between examples (especially from Standalone to Replica Set), it is recommended to run `pulumi destroy` first to avoid port or container name conflicts.

### Development Deployment

```python
from valkey_pulumi import create_standalone_valkey

dev_valkey = create_standalone_valkey(
    "dev-valkey",
    password="dev_password",
    aof_enabled=True,
    maxmemory="1gb",
    maxmemory_policy="allkeys-lru",
    disable_commands=["FLUSHDB", "FLUSHALL"]
)
```

### Production Deployment

```python
from valkey_pulumi import create_standalone_valkey

prod_valkey = create_standalone_valkey(
    "prod-valkey",
    password="secure_production_password",
    persistence_enabled=True,
    aof_enabled=True,
    aof_fsync_policy="everysec",
    maxmemory="4gb",
    maxmemory_policy="allkeys-lru",
    disable_commands=[
        "FLUSHDB", "FLUSHALL", "CONFIG", "DEBUG",
        "EVAL", "SCRIPT", "MODULE"
    ]
)
```

### Secure Deployment with TLS

```python
from valkey_pulumi import create_standalone_valkey

secure_valkey = create_standalone_valkey(
    "secure-valkey",
    password="super_secure_password",
    tls_enabled=True,
    tls_cert_file="/etc/ssl/certs/valkey.crt",
    tls_key_file="/etc/ssl/private/valkey.key",
    tls_ca_file="/etc/ssl/certs/valkey-ca.crt",
    maxmemory="2gb",
    disable_commands=["FLUSHDB", "FLUSHALL", "CONFIG"]
)
```

### High Availability Replica Set

See the [Bitnami Valkey replication documentation](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#replication) for complete details on replication configuration.

```python
from valkey_pulumi import create_valkey_replica_set

replica_set = create_valkey_replica_set(
    "ha-valkey",
    replica_count=3,
    primary_config={
        "password": "replica_password",
        "persistence_enabled": True,
        "aof_enabled": True,
        "maxmemory": "4gb",
        "replica_announce_ip": "primary.example.com"
    },
    replica_config={
        "replica_announce_ip": "replica.example.com"
    }
)
```

### ACL Configuration

```python
from valkey_pulumi import create_standalone_valkey

# Create with ACL file for fine-grained access control
acl_valkey = create_standalone_valkey(
    "acl-valkey",
    password="admin_password",
    acl_file="/etc/valkey/acl.conf",
    maxmemory="2gb"
)

# Example ACL file content:
# user default on nopass ~* +@all
# user admin on >admin_password ~* +@all
# user readonly on >readonly_password ~* +@read
```

## 🔒 Security Best Practices

### Production Security Checklist

- ✅ **Use strong passwords** with `pulumi config set --secret`
- ✅ **Enable TLS** for network encryption
- ✅ **Disable dangerous commands** (CONFIG, DEBUG, EVAL, etc.)
- ✅ **Configure memory limits** to prevent OOM issues
- ✅ **Use odd replica counts** (3, 5) to avoid split-brain
- ✅ **Set specific image versions** instead of `latest`
- ✅ **Use ACL files** for fine-grained access control

### Production Configuration

```yaml
config:
  valkey:
    image: "docker.io/bitnami/valkey:9.0.2"  # Use specific version
    password: ""  # Set with --secret
    allow_empty_password: false

    # Enhanced security
    disable_commands:
      - "FLUSHDB"
      - "FLUSHALL"
      - "CONFIG"
      - "DEBUG"
      - "EVAL"
      - "SCRIPT"
      - "MODULE"
      - "SAVE"
      - "BGSAVE"

    # Production-optimized settings
    aof_enabled: true
    aof_fsync_policy: "everysec"
    maxmemory: "4gb"
    maxmemory_policy: "allkeys-lru"
    replica_count: 3  # High availability

    # TLS security
    tls_enabled: true
    tls_cert_file: "/etc/ssl/certs/valkey.crt"
    tls_key_file: "/etc/ssl/private/valkey.key"
```

## 📚 Environment-Specific Configs

### Development (`Pulumi.dev.yaml`)

```yaml
config:
  valkey:
    image: "docker.io/bitnami/valkey:9.0"
    password: ""  # Set with dev password
    allow_empty_password: false
    persistence_enabled: true
    replica_count: 1

    # Relaxed dev settings
    aof_enabled: true
    maxmemory: null  # No memory limit for dev
    maxmemory_policy: "allkeys-lru"

    # Basic security
    disable_commands:
      - "FLUSHDB"
      - "FLUSHALL"
```

### Production (`Pulumi.prod.yaml`)

```yaml
config:
  valkey:
    image: "docker.io/bitnami/valkey:9.0.2"
    password: ""  # Set with strong production password
    allow_empty_password: false
    persistence_enabled: true
    replica_count: 3

    # Production-optimized
    aof_enabled: true
    aof_fsync_policy: "everysec"
    maxmemory: "4gb"
    maxmemory_policy: "allkeys-lru"

    # Enhanced security
    disable_commands:
      - "FLUSHDB"
      - "FLUSHALL"
      - "CONFIG"
      - "DEBUG"
      - "EVAL"
      - "SCRIPT"
      - "MODULE"

    # TLS enabled
    tls_enabled: true
    tls_cert_file: "/etc/ssl/certs/valkey.crt"
    tls_key_file: "/etc/ssl/private/valkey.key"
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install tools and create environment
mise install

# Set up development environment
invoke setup-dev

# Run all checks (format, lint, test)
invoke check
```

### Development Commands

```bash
# Format code
invoke format

# Run linting with auto-fix
invoke lint --fix

# Run tests
invoke test

# Build and serve documentation locally
invoke docs --build --open-browser

# Clean all generated files
invoke clean --all

# See all available tasks
invoke --list
```

## 📖 Configuration Reference

The configuration sections below follow the same structure as the official [Bitnami Valkey documentation](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#configuration).

### Disabling Valkey Commands

See the [Bitnami Valkey documentation on disabling commands](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#disabling-valkey-commands) for more details.

For security reasons, you may want to disable some commands. Configure the commands to disable:

```yaml
config:
  valkey:
    disable_commands: ["FLUSHDB", "FLUSHALL", "CONFIG", "DEBUG"]
```

**Pulumi Parameter:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `disable_commands` | list | `["FLUSHDB","FLUSHALL"]` | `VALKEY_DISABLE_COMMANDS` | Comma-separated list of Valkey commands to disable |

### Passing Extra Command-line Flags

See the [Bitnami Valkey documentation on passing extra flags](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#passing-extra-command-line-flags-to-valkey-server-startup) for more details.

Pass additional flags to the valkey-server startup:

```yaml
config:
  valkey:
    extra_flags: "--maxmemory 100mb --tcp-keepalive 300"
```

**Pulumi Parameter:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `extra_flags` | str | `null` | `VALKEY_EXTRA_FLAGS` | Additional flags to pass to 'valkey-server' command |

### Setting the Server Password

See the [Bitnami Valkey documentation on setting passwords](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#setting-the-server-password-on-first-run) for more details.

Configure authentication for your Valkey deployment:

```yaml
config:
  valkey:
    password: "your_secure_password"  # Use --secret when setting
    allow_empty_password: false
```

**Pulumi Parameters:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `password` | str | - | `VALKEY_PASSWORD` | Authentication password (use secret) |
| `allow_empty_password` | bool | `false` | `ALLOW_EMPTY_PASSWORD` | Allow password-less access (recommended only for development) |
| `primary_password` | str | - | `VALKEY_PRIMARY_PASSWORD` | Primary node password (for replicas) |

### Allowing Empty Passwords

See the [Bitnami Valkey documentation on allowing empty passwords](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#allowing-empty-passwords) for more details.

For development environments, you can allow empty passwords:

```yaml
config:
  valkey:
    allow_empty_password: true
```

**Warning:** This is recommended only for testing or development. Always set a strong password in production.

### Disabling AOF Persistence

See the [Bitnami Valkey documentation on disabling AOF persistence](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#disabling-aof-persistence) for more details.

Control AOF (Append Only File) persistence:

```yaml
config:
  valkey:
    aof_enabled: false
```

**Pulumi Parameters:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `aof_enabled` | bool | `true` | `VALKEY_AOF_ENABLED` | Enable AOF persistence |
| `aof_fsync_policy` | str | `"everysec"` | Config file | AOF fsync policy (always/everysec/no) |

### Enabling Access Control List (ACL)

See the [Bitnami Valkey documentation on ACL](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#enabling-access-control-list) for more details.

Configure fine-grained access control:

```yaml
config:
  valkey:
    acl_file: "/opt/bitnami/valkey/mounted-etc/users.acl"
```

**Pulumi Parameter:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `acl_file` | str | - | `VALKEY_ACLFILE` | Path to ACL configuration file |

### Setting Up a Standalone Instance

See the [Bitnami Valkey documentation on standalone instances](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#setting-up-a-standalone-instance) for more details.

Configure basic standalone Valkey deployment:

```yaml
config:
  valkey:
    port: 6379
    database: "valkey"
    valkey_data_dir: "/bitnami/valkey/data"
```

**Pulumi Parameters:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `image` | str | `docker.io/bitnami/valkey:9.0` | - | Docker image |
| `port` | int | `6379` | `VALKEY_PORT_NUMBER` | Valkey port number |
| `database` | str | `valkey` | `VALKEY_DATABASE` | Default Valkey database |
| `valkey_data_dir` | str | `/bitnami/valkey/data` | `VALKEY_DATA_DIR` | Valkey data directory |
| `valkey_overrides_file` | str | `${VALKEY_MOUNTED_CONF_DIR}/overrides.conf` | `VALKEY_OVERRIDES_FILE` | Valkey config overrides file |

### Setting Up Replication

See the [Bitnami Valkey documentation on replication](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#setting-up-replication) for more details.

Configure primary/replica replication:

```yaml
config:
  valkey:
    replication_mode: "primary"  # or "replica"
    primary_host: "valkey-primary"  # for replicas
    primary_port_number: 6379
    replica_ip: "10.0.1.100"  # optional
    replica_port: 6379  # optional
```

**Pulumi Parameters:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `replication_mode` | str | `nil` | `VALKEY_REPLICATION_MODE` | Replication mode (primary/replica) |
| `primary_host` | str | `nil` | `VALKEY_PRIMARY_HOST` | Primary host (for replicas) |
| `primary_port_number` | int | `6379` | `VALKEY_PRIMARY_PORT_NUMBER` | Primary host port (for replicas) |
| `replica_ip` | str | `nil` | `VALKEY_REPLICA_IP` | Replication announce IP |
| `replica_port` | int | `nil` | `VALKEY_REPLICA_PORT` | Replication announce port |
| `replica_count` | int | `1` | - | Number of replicas (Pulumi-specific) |

### Securing Valkey Traffic (TLS/SSL)

See the [Bitnami Valkey documentation on TLS/SSL](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#securing-valkey-traffic) for more details.

Enable TLS encryption for Valkey traffic:

```yaml
config:
  valkey:
    tls_enabled: true
    tls_port_number: 6380
    tls_cert_file: "/opt/bitnami/valkey/certs/valkey.crt"
    tls_key_file: "/opt/bitnami/valkey/certs/valkey.key"
    tls_ca_file: "/opt/bitnami/valkey/certs/valkeyCA.crt"
    tls_auth_clients: true
```

**TLS/SSL Parameters:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `tls_enabled` | bool | `false` | `VALKEY_TLS_ENABLED` | Enable TLS |
| `tls_port_number` | int | `6379` | `VALKEY_TLS_PORT_NUMBER` | TLS port number |
| `tls_cert_file` | str | - | `VALKEY_TLS_CERT_FILE` | Path to TLS certificate file |
| `tls_key_file` | str | - | `VALKEY_TLS_KEY_FILE` | Path to TLS key file |
| `tls_ca_file` | str | - | `VALKEY_TLS_CA_FILE` | Path to TLS CA file |
| `tls_ca_dir` | str | - | `VALKEY_TLS_CA_DIR` | Directory containing TLS CA certificates |
| `tls_key_file_pass` | str | - | `VALKEY_TLS_KEY_FILE_PASS` | TLS key file passphrase |
| `tls_dh_params_file` | str | - | `VALKEY_TLS_DH_PARAMS_FILE` | TLS DH parameters file |
| `tls_auth_clients` | bool | `yes` | `VALKEY_TLS_AUTH_CLIENTS` | Require client authentication |

### Configuration File and Overrides

See the [Bitnami Valkey documentation on configuration files](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#configuration-file) and [overriding configuration](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#overriding-configuration) for more details.

Use custom configuration files:

```yaml
config:
  valkey:
    valkey_config_file: "/path/to/custom-valkey.conf"
    # or use overrides file
    valkey_overrides_file: "/opt/bitnami/valkey/mounted-etc/overrides.conf"
```

**Configuration File Parameters:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `valkey_config_file` | str | - | Custom | Path to custom Valkey configuration file for advanced settings |
| `valkey_overrides_file` | str | `${VALKEY_MOUNTED_CONF_DIR}/overrides.conf` | `VALKEY_OVERRIDES_FILE` | Valkey config overrides file |

### Enable Valkey RDB Persistence

See the [Bitnami Valkey documentation on RDB persistence](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#enable-valkey-rdb-persistence) for more details.

Configure RDB snapshot persistence:

```yaml
config:
  valkey:
    rdb_policy_disabled: false
    rdb_policy: "900#1 600#5 300#10 120#50 60#1000 30#10000"
```

**RDB Persistence Parameters:**
| Parameter | Type | Default | Environment Variable | Description |
|-----------|------|---------|---------------------|-------------|
| `rdb_policy` | str | `null` | `VALKEY_RDB_POLICY` | RDB persistence policy |
| `rdb_policy_disabled` | bool | `no` | `VALKEY_RDB_POLICY_DISABLED` | Disable RDB persistence |

### Performance and Advanced Configuration

Configure performance tuning and advanced settings:

```yaml
config:
  valkey:
    # Memory management
    maxmemory: "2gb"
    maxmemory_policy: "allkeys-lru"

    # Connection settings
    timeout: 300
    tcp_keepalive: 60

    # Logging
    valkey_log_level: "notice"

    # Performance
    io_threads: 4
    io_threads_do_reads: true

    # Client buffer limits
    client_output_buffer_limit_normal: "0 0 0"
    client_output_buffer_limit_slave: "256mb 64mb 60"
    client_output_buffer_limit_pubsub: "32mb 8mb 60"
```

**Advanced Parameters:**
| Parameter | Type | Default | Implementation | Description |
|-----------|------|---------|----------------|-------------|
| **Memory Management** | | | | |
| `maxmemory` | str | `null` | Valkey config | Maximum memory limit |
| `maxmemory_policy` | str | `"allkeys-lru"` | Valkey config | Memory eviction policy |
| **Connection Settings** | | | | |
| `timeout` | int | `300` | Valkey config | Client timeout (seconds) |
| `tcp_keepalive` | int | `60` | Valkey config | TCP keepalive (seconds) |
| `allow_remote_connections` | bool | `yes` | `VALKEY_ALLOW_REMOTE_CONNECTIONS` | Allow remote connections |
| **Logging** | | | | |
| `valkey_log_level` | str | `"notice"` | Valkey config | Valkey log level |
| **Performance** | | | | |
| `io_threads` | int | `null` | `VALKEY_IO_THREADS` | Number of I/O threads |
| `io_threads_do_reads` | bool | `null` | `VALKEY_IO_THREADS_DO_READS` | Enable multithreading for reads |
| **Client Buffer Limits** | | | | |
| `client_output_buffer_limit_normal` | str | `"0 0 0"` | Valkey config | Normal client buffer limits |
| `client_output_buffer_limit_slave` | str | `"256mb 64mb 60"` | Valkey config | Replica client buffer limits |
| `client_output_buffer_limit_pubsub` | str | `"32mb 8mb 60"` | Valkey config | Pub/sub client buffer limits |
| **Other Settings** | | | | |
| `databases` | int | `16` | Valkey config | Number of databases |
| `protected_mode` | bool | `true` | Valkey config | Enable protected mode |

## 📊 Post-Deployment Checklist

### 1. Verify Connectivity

```bash
# Test connection from application server
redis-cli -h <valkey_host> -p 6379 -a <password> ping

# Verify replica status
redis-cli -h <valkey_host> -p 6379 -a <password> info replication

# Check configuration
redis-cli -h <valkey_host> -p 6379 -a <password> config get save
```

### 2. Monitor Resources

Monitor these key metrics:
- Memory usage
- CPU utilization
- Connected clients
- Command statistics
- Replication lag
- Error rates

**Alert Thresholds:**
- Memory > 80%
- CPU > 75%
- Replication lag > 5 seconds
- Connection errors > 1% of requests

### 3. Test Failover

For replica sets, test failover scenarios:
```bash
# Check replica status
redis-cli -h <replica_host> -p <replica_port> -a <password> info replication

# Test manual failover (if using Redis Sentinel)
redis-cli -h <sentinel_host> -p <sentinel_port> sentinel failover <master_name>
```

## 🔧 Troubleshooting

### Common Issues

1. **Out of Memory**
   ```bash
   # Check memory usage
   redis-cli -h <host> -p 6379 -a <password> info memory

   # Check maxmemory policy
   redis-cli -h <host> -p 6379 -a <password> config get maxmemory-policy
   ```

2. **Replication Lag**
   ```bash
   # Check replication status
   redis-cli -h <host> -p 6379 -a <password> info replication

   # Check network connectivity between primary and replicas
   ```

3. **Connection Refused**
   ```bash
   # Check if container is running
   docker ps | grep valkey

   # Check port configuration and firewall rules
   netstat -tlnp | grep 6379
   ```

4. **Authentication Issues**
   ```bash
   # Verify password is set correctly
   redis-cli -h <host> -p 6379 -a <password> ping

   # Check if password is required
   redis-cli -h <host> -p 6379 ping  # Should return NOAUTH Authentication required
   ```

### Emergency Procedures

1. **Data Recovery** - Use AOF files for point-in-time recovery
2. **Failover** - Manually promote replica if primary fails
3. **Password Reset** - Update configuration and restart containers

### Maintenance

**Regular Tasks:**
- Security updates: Update Docker image monthly
- Backup verification: Test restore procedures quarterly
- Performance tuning: Adjust memory policies based on usage
- Log review: Check for errors or unusual activity

**Scaling:**
- Add more replicas for read scaling
- Upgrade instance size for memory/CPU needs
- Consider sharding for very large datasets

## 🚀 Deployment Commands

### Basic Deployment

```bash
# Initialize stack
pulumi stack init dev

# Preview deployment
pulumi preview

# Deploy
pulumi up

# Get outputs
pulumi stack output
```

### Production Deployment

```bash
# Use production stack
pulumi stack select prod

# Set production password
pulumi config set --secret valkey:password "strong_production_password"

# Set production-specific settings
pulumi config set valkey:maxmemory "4gb"
pulumi config set valkey:replica_count 3
pulumi config set valkey:tls_enabled true

# Deploy to production
pulumi up
```

## 📚 Additional Documentation

### Bitnami Valkey References

This Pulumi component is based on the official [Bitnami Valkey container](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md). Key sections:

- **[Main Documentation](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md)** - Complete reference
- **[Configuration](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#configuration)** - All environment variables
- **[Persistence](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#persistence)** - AOF and RDB settings
- **[Security](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#security)** - Authentication and access control
- **[Replication](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#replication)** - Primary-replica setup
- **[Logging](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#logging)** - Log configuration
- **[TLS/SSL](https://github.com/bitnami/containers/blob/main/bitnami/valkey/README.md#securing-traffic-using-tls)** - Encryption setup

### Project Documentation

For detailed documentation about this Pulumi component, see the `docs/` directory:
- [**API Documentation**](docs/api.md) - Complete API reference
- [**Development Guide**](docs/development.md) - Contributing and development setup
- [**Contributing Guide**](docs/contributing.md) - How to contribute to the project

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`invoke check`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/daotl/valkey-pulumi/issues)
- **Documentation**: [Project Documentation][documentation]
- **Questions**: Feel free to open an issue for questions

---

[badge-tests]: https://img.shields.io/github/actions/workflow/status/daotl/valkey-pulumi/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/valkey-pulumi
[tests]: https://github.com/daotl/valkey-pulumi/actions/workflows/test.yaml
[documentation]: https://valkey-pulumi.readthedocs.io
[mise]: https://mise.dev/
