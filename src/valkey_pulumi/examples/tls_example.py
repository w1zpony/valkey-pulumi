"""Example: Valkey with TLS encryption enabled.

This demonstrates how to deploy Valkey with TLS certificates for secure communication.
"""

from valkey_pulumi import create_standalone_valkey

# Create Valkey with TLS enabled
tls_valkey = create_standalone_valkey(
    "secure-valkey",
    password="super_secure_tls_password",
    tls_enabled=True,
    tls_cert_file="/etc/ssl/certs/valkey.crt",
    tls_key_file="/etc/ssl/private/valkey.key",
    tls_ca_file="/etc/ssl/certs/valkey-ca.crt",
    port=6379,
    persistence_enabled=True,
    disable_commands=["FLUSHDB", "FLUSHALL", "CONFIG"],
)

# For this example to work, you need:
# 1. TLS certificate files at the specified paths
# 2. Or modify paths to match your certificate locations
# 3. Set password using: pulumi config set --secret valkey:password "your_password"

print("TLS-enabled Valkey deployment configured!")
print("Connect using: redis-cli --tls -h <host> -p 6379 -a <password> --cacert /etc/ssl/certs/valkey-ca.crt")
