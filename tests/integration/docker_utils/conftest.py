import os

import pytest

from localstack.config import is_env_not_false
from localstack.utils.container_utils.container_client import ContainerClient
from localstack.utils.container_utils.docker_cmd_client import CmdDockerClient
from localstack.utils.container_utils.docker_sdk_client import SdkDockerClient


def _check_skip(client: ContainerClient):
    if not is_env_not_false("SKIP_DOCKER_TESTS"):
        pytest.skip("SKIP_DOCKER_TESTS is set")

    if not client.has_docker():
        pytest.skip("Docker is not available")


@pytest.fixture(
    params=[CmdDockerClient(), SdkDockerClient()], ids=["CmdDockerClient", "SdkDockerClient"]
)
def docker_client(request):
    client = request.param
    _check_skip(
        client
    )  # this is a hack to get a global skip for all tests that require the docker client
    yield client


def is_podman_test():
    return os.environ.get("DOCKER_CMD") == "podman"


# marker to indicate tests that don't work against Podman (i.e., should only be run against Docker)
skip_for_podman = pytest.mark.skipif(
    is_podman_test(),
    reason="Test not applicable when run against Podman (only Docker)",
)
