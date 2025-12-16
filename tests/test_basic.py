import os
import sys
from pathlib import Path

import valkey_pulumi
from valkey_pulumi.__main__ import _build_env
from valkey_pulumi.config import DEFAULT_VALKEY_CONFIG, Config

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

try:
    import pulumi  # type: ignore
    import pulumi_docker  # type: ignore
except ImportError:  # pragma: no cover - test shim
    import types

    pulumi = types.ModuleType("pulumi")

    class _Config:
        def get(self, *_args, **_kwargs):
            return None

        def get_bool(self, *_args, **_kwargs):
            return None

        def get_int(self, *_args, **_kwargs):
            return None

        def get_object(self, *_args, **_kwargs):
            return None

        def get_list(self, *_args, **_kwargs):
            return None

        def get_secret(self, *_args, **_kwargs):
            return None

    class _ResourceOptions:
        def __init__(self, **_kwargs):
            pass

    def _export(*_args, **_kwargs):
        return None

    pulumi.Config = _Config  # type: ignore[attr-defined]
    pulumi.ResourceOptions = _ResourceOptions  # type: ignore[attr-defined]
    pulumi.export = _export  # type: ignore[attr-defined]
    sys.modules["pulumi"] = pulumi

    pulumi_docker = types.ModuleType("pulumi_docker")

    class _EnvArgs:
        def __init__(self, name: str, value: str):
            self.name = name
            self.value = value

    pulumi_docker.ContainerEnvironmentArgs = _EnvArgs  # type: ignore[attr-defined]
    sys.modules["pulumi_docker"] = pulumi_docker
else:
    import pulumi_docker  # type: ignore


def _env_dict(envs):
    return {env.name: env.value for env in envs}


def test_package_has_version():
    assert valkey_pulumi.__version__ is not None


def test_build_env_uses_defaults_and_sets_data_dir():
    envs = _build_env(Config())
    env_map = _env_dict(envs)

    assert env_map["VALKEY_DATA_DIR"] == DEFAULT_VALKEY_CONFIG["valkey_data_dir"]
    assert env_map["VALKEY_PORT_NUMBER"] == str(DEFAULT_VALKEY_CONFIG["port"])
    assert env_map["VALKEY_ALLOW_REMOTE_CONNECTIONS"] == "yes"


def test_build_env_replication_tls_and_acl_paths_are_mapped():
    cfg = Config(
        replication_mode="replica",
        primary_host="primary",
        primary_port_number=6381,
        tls_enabled=True,
        tls_cert_file="/tmp/cert.pem",
        tls_key_file="/tmp/key.pem",
        tls_ca_file="/tmp/ca.pem",
        acl_file="/tmp/users.acl",
    )
    env_map = _env_dict(_build_env(cfg))

    assert env_map["VALKEY_REPLICATION_MODE"] == "replica"
    assert env_map["VALKEY_PRIMARY_HOST"] == "primary"
    assert env_map["VALKEY_PRIMARY_PORT_NUMBER"] == "6381"
    assert env_map["VALKEY_TLS_ENABLED"] == "yes"
    assert env_map["VALKEY_TLS_CERT_FILE"] == os.path.abspath("/tmp/cert.pem")
    assert env_map["VALKEY_TLS_KEY_FILE"] == os.path.abspath("/tmp/key.pem")
    assert env_map["VALKEY_TLS_CA_FILE"] == os.path.abspath("/tmp/ca.pem")
    assert env_map["VALKEY_ACLFILE"] == "/opt/bitnami/valkey/mounted-etc/users.acl"


def test_build_env_primary_password_is_propagated():
    cfg = Config(replication_mode="replica", primary_password="secret", password="secret")
    env_map = _env_dict(_build_env(cfg))

    assert env_map["VALKEY_PRIMARY_PASSWORD"] == "secret"
    assert env_map["VALKEY_PASSWORD"] == "secret"


def test_build_env_allow_empty_and_extra_flags():
    cfg = Config(allow_empty_password=True, extra_flags=["--foo", "--bar"])
    env_map = _env_dict(_build_env(cfg))

    assert env_map["ALLOW_EMPTY_PASSWORD"] == "yes"
    assert env_map["VALKEY_EXTRA_FLAGS"] == "--foo --bar"


def test_build_env_overrides_path_and_tls_auth_toggle():
    cfg = Config(
        valkey_overrides_file="/tmp/overrides.conf",
        tls_enabled=True,
        tls_auth_clients=False,
    )
    env_map = _env_dict(_build_env(cfg))

    assert env_map["VALKEY_OVERRIDES_FILE"] == "/opt/bitnami/valkey/mounted-etc/overrides.conf"
    assert env_map["VALKEY_TLS_ENABLED"] == "yes"
    assert env_map["VALKEY_TLS_AUTH_CLIENTS"] == "no"
