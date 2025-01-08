import traceback
import unittest
from click.testing import CliRunner
from nl_service_metadata_generator.cli import cli
from nl_service_metadata_generator.enums import ServiceType, InspireType, SdsType
from nl_service_metadata_generator.constants import DEFAULT_CSW_ENDPOINT
from pathlib import Path

CONSTANTS_CONFIG_FILE = Path('../../../example_json/constants.json')
EXAMPLE_HVD_INPUT = Path('../../../example_json/hvd.json')
EXPECTED_HVD_OUTPUT = Path('data/expected_hvd.xml')
OUTPUT = Path('./test.xml')


class TestMetaDataWithHVDCategories(unittest.TestCase):

    # def tearDown(self):
    #     # if OUTPUT.exists():
    #     #     OUTPUT.unlink()

    def test_hallo(self):
        # Initialize the CLI runner
        runner = CliRunner()

        # Invoke the 'hallo' command
        result = runner.invoke(cli, ['hallo'])

        # Assertions
        self.assertEqual(result.exit_code, 0)  # Ensure the command exits successfully
        self.assertIn('yolo', result.output)

    def test_with_lower_category(self):
        runner = CliRunner(mix_stderr=False)

        # Convert enum values to strings for CLI arguments
        result = runner.invoke(
            cli,
            [
                'generate',
                ServiceType.WMS.value,
                InspireType.NONE.value,
                str(CONSTANTS_CONFIG_FILE),
                str(EXAMPLE_HVD_INPUT),
                str(OUTPUT),
            ]
        )

        # Check if the command executed without exceptions
        self.assertEqual(0, result.exit_code, f"Command Should not fail:\n "+ ''.join(traceback.format_exception(*result.exc_info)))

        # Check content of the output file
        self.assertTrue(OUTPUT.exists(), "Output file should be created")
        # self.assertEqual(EXPECTED_HVD_OUTPUT.read_text(), OUTPUT.read_text(), 'HVD XML should be equal to expected XML output')


if __name__ == '__main__':
    unittest.main()