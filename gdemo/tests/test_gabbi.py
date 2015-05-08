"""A test module to load gabbi-demo tests."""

import os
import sys

from gabbi import driver
from gabbi import fixture

from gdemo import load_app
from gdemo import DATA_STORE

TESTS_DIR = 'gabbits'
NAMES = [u'alpha', u'beta', u'gamma', u'delta', u'epsilon', u'zeta']


class SampleDataFixture(fixture.GabbiFixture):

    def start_fixture(self):
        """Create some sample data"""
        objects = {}
        for name in NAMES:
            object_data = {'type': 'text/plain',
                           'body': name.encode('UTF-8')}
            objects[name] = object_data
        DATA_STORE['fixtured'] = {'owner': 'this',
                                  'objects': objects}

    def stop_fixture(self):
        try:
            del DATA_STORE['fixtured']
        except KeyError:
            pass


def load_tests(loader, tests, pattern):
    """Provide a TestSuite to the discovery process."""
    test_dir = os.path.join(os.path.dirname(__file__), TESTS_DIR)
    return driver.build_tests(test_dir, loader, host=None,
                              intercept=load_app,
                              fixture_module=sys.modules[__name__])
