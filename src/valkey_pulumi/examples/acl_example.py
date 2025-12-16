"""Example: Valkey with Access Control List (ACL) configuration.

This demonstrates how to deploy Valkey with fine-grained access control using ACL files.
"""

from valkey_pulumi import create_standalone_valkey

# Create Valkey with ACL file for fine-grained access control
acl_valkey = create_standalone_valkey(
    "acl-valkey",
    password="admin_password",
    acl_file="/etc/valkey/acl.conf",  # Path to ACL configuration file
    port=6379,
    persistence_enabled=True,
    disable_commands=["CONFIG", "DEBUG", "EVAL"],
)

# Example ACL file content (save as /etc/valkey/acl.conf):
"""
# ACL file example
# Format: user <username> on/off [password] [pattern] [+commands] [-commands] [keys] [channels]

# Default user with full access (remove for production)
user default on nopass ~* +@all

# Admin user with full access
user admin on >admin_password ~* +@all

# Read-only user for analytics
user readonly on >readonly_password ~* +@read -@write

# App-specific user with limited access
user app_user on >app_password ~app:* +@read +@write +@string +@hash +@list +@set +@sorted_set

# Replication user
user replica on >replica_password ~* +@read +@replica

# Pub/sub user
user pubsub_user on >pubsub_password ~* +@pubsub ~channel*

# Limited user for specific keys only
user limited_user on >limited_password ~data:specific:* +get +set +hget +hset
"""

print("ACL-enabled Valkey deployment configured!")
print("Create an ACL file at /etc/valkey/acl.conf with rules like the example above")
print("Connect as admin: redis-cli -h <host> -p 6379 -a admin_password")
print("Test ACL: ACL LIST")
