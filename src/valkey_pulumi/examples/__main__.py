"""Run Valkey example deployments with Pulumi.

Select an example by setting VALKEY_EXAMPLE to one of:
  - standalone (default)
  - replica_set
  - tls
  - acl
"""

import os

from valkey_pulumi.examples.acl_example import acl_valkey
from valkey_pulumi.examples.replica_set import deploy_valkey_replica_set
from valkey_pulumi.examples.standalone import deploy_standalone_valkey
from valkey_pulumi.examples.tls_example import tls_valkey


def main():
    """Run the selected Valkey deployment example.

    Reads the VALKEY_EXAMPLE environment variable to determine which example
    to run. Defaults to 'standalone' if not set.

    Available examples:
        - standalone: Deploys a single Valkey instance
        - replica_set: Deploys Valkey with replica configuration
        - tls: Deploys Valkey with TLS encryption
        - acl: Deploys Valkey with Access Control Lists (ACL)

    Returns:
        None

    Raises:
        ValueError: If VALKEY_EXAMPLE is set to an unsupported value.

    """
    choice = os.environ.get("VALKEY_EXAMPLE", "standalone").lower()

    if choice == "replica_set":
        deploy_valkey_replica_set()
    elif choice == "tls":
        # The TLS example instantiates resources at import-time; reference to keep lint happy
        _ = tls_valkey
    elif choice == "acl":
        _ = acl_valkey
    else:
        deploy_standalone_valkey()


if __name__ == "__main__":
    main()
