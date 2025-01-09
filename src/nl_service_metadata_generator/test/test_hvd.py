import os
import traceback
import unittest
from click.testing import CliRunner
from nl_service_metadata_generator.cli import cli
from nl_service_metadata_generator.enums import ServiceType, InspireType
from pathlib import Path

CONSTANTS_CONFIG_FILE = Path('../../../example_json/constants.json')
EXPECTED_PATH: Path = Path('data/expected')
INPUT_PATH: Path = Path('data/input')
OUTPUT_PATH: Path = Path('data/output')

class UnitTestDataPath:

    def __init__(self, name, service_type: ServiceType):
        self.input = INPUT_PATH / (name if name.endswith('.json') else name + '.json')
        result_path = self.input.stem + '_' + service_type.value + '.xml'
        self.output = OUTPUT_PATH / result_path
        self.expected = EXPECTED_PATH / result_path


def format_exception(e):
    return ''.join(traceback.format_exception(*e))

class TestNLServiceMetadataGeneratorCLI(unittest.TestCase):

    def setUp(self):
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        self.runner = CliRunner(mix_stderr=False)

    def assertCLIOutput(self, result, test_path):
        self.assertEqual(0, result.exit_code, f"Command Should execute without exceptions:\n " + format_exception(result.exc_info))
        self.assertTrue(test_path.output.exists(), "Output file should be created")
        self.assertEqual(test_path.expected.read_text(), test_path.output.read_text(),f'Generated metadata in {test_path.output} should be equal to expected metadata in {test_path.expected}')

    def test_hvd_simple(self):
        test_path = UnitTestDataPath('hvd_simple', ServiceType.WMS)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.WMS.value,
                InspireType.NONE.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

    def test_hvd_complex(self):
        test_path = UnitTestDataPath('hvd_complex', ServiceType.WMS)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.WMS.value,
                InspireType.NONE.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

    def test_inspire_wms(self):
        test_path = UnitTestDataPath('inspire', ServiceType.WMS)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.WMS.value,
                InspireType.NETWORK.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

    def test_inspire_wfs(self):
        test_path = UnitTestDataPath('inspire', ServiceType.WFS)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.WFS.value,
                InspireType.NETWORK.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

    def test_inspire_atom(self):
        test_path = UnitTestDataPath('inspire', ServiceType.ATOM)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.ATOM.value,
                InspireType.NETWORK.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

    def test_oaf(self):
        test_path = UnitTestDataPath('oaf', ServiceType.OAF)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.OAF.value,
                InspireType.NONE.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

    def test_oat(self):
        test_path = UnitTestDataPath('oat', ServiceType.OAT)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.OAT.value,
                InspireType.NONE.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

    def test_regular_wms(self):
        test_path = UnitTestDataPath('regular', ServiceType.WMS)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.WMS.value,
                InspireType.NONE.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

    def test_regular_wfs(self):
        test_path = UnitTestDataPath('regular', ServiceType.WFS)

        result = self.runner.invoke(
            cli,
            [
                'generate',
                ServiceType.WFS.value,
                InspireType.NONE.value,
                str(CONSTANTS_CONFIG_FILE),
                str(test_path.input),
                str(test_path.output),
            ]
        )

        self.assertCLIOutput(result, test_path)

if __name__ == '__main__':
    unittest.main()