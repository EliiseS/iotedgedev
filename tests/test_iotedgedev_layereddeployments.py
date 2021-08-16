from iotedgedev.envvars import EnvVars
from iotedgedev.output import Output
import os
import pytest
from .utility import (
    get_platform_type,
    runner_invoke,
)

pytestmark = pytest.mark.e2e

tests_dir = os.path.join(os.getcwd(), "tests")
test_solution_shared_lib_dir = os.path.join(tests_dir, "assets", "test_solution_shared_lib")


@pytest.fixture(scope="module", autouse=True)
def setup_dotenv():
    output = Output()
    envvars = EnvVars(output)
    envvars.set_envvar("MODULES_PATH", "../test_solution_shared_lib/modules")


@pytest.mark.parametrize(
    "test_file_name",
    [
        ("layered_deployment.template.json"),
        ("layered_deployment.template_with_flattened_props.json"),
    ],
)
def test_build_and_push(test_file_name):
    os.chdir(test_solution_shared_lib_dir)

    result = runner_invoke(['build', '--push', '-f', f'../layered_deployment_templates/{test_file_name}', '-P', get_platform_type()])

    assert 'sample_module:0.0.1-RC' in result.output
    assert 'BUILD COMPLETE' in result.output
    assert 'PUSH COMPLETE' in result.output
    assert 'ERROR' not in result.output
