import pytest
import sys
import io
import subprocess
import os
import re

def pytest_addoption(parser):
    parser.addoption(
        "--output-file", action="store", default="test_output.log", help="Path to the output file"
    )

def strip_ansi_codes(text):
    """Remove ANSI escape sequences from text."""
    ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mK]')
    return ansi_escape.sub('', text)

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Check if this is a rerun
    if os.environ.get('PYTEST_RERUN', '0') == '1':
        return  # Skip configuration if it's a rerun

    output_file = config.getoption("output_file")
    
    # Open the file for writing with UTF-8 encoding
    config.output_file_handle = open(output_file, "w", encoding="utf-8")
    
    # Create a StringIO stream to capture output
    config.output_buffer = io.StringIO()
    
    # Set an environment variable to track rerun status
    os.environ['PYTEST_RERUN'] = '0'

    # Redirect stdout and stderr to the StringIO buffer
    sys.stdout = config.output_buffer
    sys.stderr = config.output_buffer

    # Capture the pytest command and arguments
    pytest_command = ' '.join(sys.argv)
    print(f"Running command: {pytest_command}")

@pytest.hookimpl(tryfirst=True)
def pytest_unconfigure(config):
    # Restore the original stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    # Check if output_buffer was initialized
    if hasattr(config, 'output_buffer'):
        # Write the buffer content to the log file without ANSI codes
        log_content = config.output_buffer.getvalue()
        stripped_log_content = strip_ansi_codes(log_content)
        config.output_file_handle.write(stripped_log_content)

        # Close the output file handle and the StringIO buffer
        config.output_file_handle.close()
        config.output_buffer.close()

    # Automatically rerun the tests if they haven't been rerun yet
    if os.environ['PYTEST_RERUN'] == '0':
        os.environ['PYTEST_RERUN'] = '1'  # Set the environment variable to prevent further reruns
        subprocess.run(['pytest'] + sys.argv[1:])  # Rerun without --output-file
