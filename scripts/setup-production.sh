#!/bin/bash

# Production setup script for Valkey deployment
# This script helps configure the production stack

set -e

echo "=== Valkey Production Setup Script ==="
echo

# Check if Pulumi is installed
if ! command -v pulumi &> /dev/null; then
    echo "ERROR: Pulumi CLI is not installed. Please install it first."
    echo "Visit: https://www.pulumi.com/docs/get-started/install/"
    exit 1
fi

# Function to generate a strong password
generate_password() {
    openssl rand -base64 48 | tr -d "=+/" | cut -c1-32
}

# Select production stack
echo "1. Selecting production stack..."
pulumi stack select prod
echo "✓ Production stack selected"
echo

# Set secure password
echo "2. Setting secure Valkey password..."
if pulumi config get valkey:password >/dev/null 2>&1; then
    echo "Password already set. Skipping..."
else
    PASSWORD=$(generate_password)
    pulumi config set --secret valkey:password "$PASSWORD"
    echo "✓ Secure password generated and set"
    echo "  Password: $PASSWORD"
    echo "  IMPORTANT: Save this password securely!"
fi
echo

# Check and set other important configurations
echo "3. Checking production configuration..."

# Check image version
IMAGE_VERSION=$(pulumi config get valkey:image 2>/dev/null || echo "not set")
if [[ "$IMAGE_VERSION" == *"latest"* ]] || [[ "$IMAGE_VERSION" == *"9.0"* ]]; then
    echo "⚠️  WARNING: Consider using a specific version tag instead of '$IMAGE_VERSION'"
    echo "   Example: docker.io/bitnami/valkey:9.0.2"
    read -p "   Do you want to set a specific version? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "   Enter version tag (e.g., 9.0.2): " VERSION
        pulumi config set valkey:image "docker.io/bitnami/valkey:$VERSION"
        echo "✓ Image version set to: docker.io/bitnami/valkey:$VERSION"
    fi
else
    echo "✓ Image version: $IMAGE_VERSION"
fi

# Check replica count
REPLICA_COUNT=$(pulumi config get valkey:replica_count 2>/dev/null || echo "not set")
if [[ "$REPLICA_COUNT" == "not set" ]] || [[ "$REPLICA_COUNT" -lt 3 ]]; then
    echo "⚠️  WARNING: Production should have at least 3 replicas for high availability"
    read -p "   Do you want to set replica count to 3? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pulumi config set valkey:replica_count 3
        echo "✓ Replica count set to 3"
    fi
else
    echo "✓ Replica count: $REPLICA_COUNT"
fi

# Check memory configuration
MAXMEMORY=$(pulumi config get valkey:extra_env_vars.VALKEY_MAXMEMORY 2>/dev/null || echo "not set")
if [[ "$MAXMEMORY" == "not set" ]]; then
    echo "⚠️  WARNING: Memory limit not configured"
    read -p "   Do you want to set memory limit to 2gb? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pulumi config set valkey:extra_env_vars.VALKEY_MAXMEMORY "2gb"
        echo "✓ Memory limit set to 2gb"
    fi
else
    echo "✓ Memory limit: $MAXMEMORY"
fi

echo
echo "4. Production setup summary:"
echo "   Stack: $(pulumi stack current)"
echo "   Password: $(pulumi config get valkey:password >/dev/null 2>&1 && echo "✓ Set" || echo "✗ Not set")"
echo "   Image: $(pulumi config get valkey:image 2>/dev/null || echo "Using default")"
echo "   Replicas: $(pulumi config get valkey:replica_count 2>/dev/null || echo "Using default")"

echo
echo "=== Next Steps ==="
echo "1. Review and modify Pulumi.prod.yaml if needed"
echo "2. Run 'pulumi preview' to see what will be deployed"
echo "3. Run 'pulumi up' when ready to deploy"
echo "4. Read PRODUCTION.md for detailed deployment guidance"
echo
echo "✓ Production setup complete!"
