"""Prepare files for conversion."""

# Import hsntools functionality
from hsntools.paths import Paths
from hsntools.io.custom import load_configs, save_config, save_object

from hsntools.io.utils import get_files, make_session_name
from hsntools.run import print_status

# Add local code folder and import any needed code from local `conv` module
import sys
sys.path.append('..')
from conv.parser import process_session

# Import settings (from local folder)
from settings import PROJECT_PATH, SESSION, SETTINGS

###################################################################################################
###################################################################################################

def prepare_data(SESSION=SESSION, SETTINGS=SETTINGS):
    """Prepare a session of data for NWB conversion."""

    # Initialize paths
    paths = Paths(PROJECT_PATH, SESSION['SUBJECT'], SESSION['EXPERIMENT'], SESSION['SESSION'])

    # Define the session name
    session_name = make_session_name(SESSION['SUBJECT'], SESSION['EXPERIMENT'], SESSION['SESSION'])

    print_status(SETTINGS['VERBOSE'], '\nPREPARING XX DATA\n', 0)
    print_status(SETTINGS['VERBOSE'], 'Preparing data for {}'.format(session_name), 0)

    ## PARSE LOG FILE

    if SETTINGS['PARSE_LOG']:

        task = process_session(paths, process=True, verbose=SETTINGS['VERBOSE'])
        save_object(task, session_name, folder=paths.task)

    ## COLLECT METADATA

    print_status(SETTINGS['VERBOSE'], 'preparing metadata files...', 1)

    # Get a list of the available metadata files, and load them
    metadata_files = get_files('../metadata/', select='yaml')
    metadata = load_configs(metadata_files, '../metadata/')

    # Save out the collected config file for the session
    save_config(metadata, session_name, folder=paths.metadata)

    print_status(SETTINGS['VERBOSE'],
                 'Completed data preparation for {}\n'.format(session_name), 0)


if __name__ == '__main__':
    prepare_data()
