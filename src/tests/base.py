import unittest
import subprocess
import os
import sys
import io
import time

from cx2d_lib import get_error_indicator

PY3 = sys.version_info[0] == 3

# Time old last exec output
RECENT_FILE_S = 1.0

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_EXAMPLE_LEGACY = os.path.abspath(THIS_PATH+"/../../examples/run_example_vgos.sh")
PATH_EXAMPLE_NUMERIC = os.path.abspath(THIS_PATH+"/../../examples/run_example_vgos_num.sh")
PATH_BASE = os.path.abspath(THIS_PATH+"/../../")
PATH_OUT = THIS_PATH+"/../../output"
PATH_SRC = THIS_PATH+"/../../src"

EXAMPLES = THIS_PATH+"/../../examples/test_dataset_vgos/example_output/"

REF_FILE_PY2_LEGACY = EXAMPLES + "OUT_s0_v0_python2_sort_legacy.out"
REF_FILE_PY3_LEGACY = EXAMPLES + "OUT_s0_v0_python3_sort_legacy.out"
REF_FILE_PY2_NUMERIC = EXAMPLES + "OUT_s0_v0_python2_sort_numeric.out"
REF_FILE_PY3_NUMERIC = EXAMPLES + "OUT_s0_v0_python3_sort_numeric.out"

if not PY3:
    REF_FILE_LEGACY = REF_FILE_PY2_LEGACY
    REF_FILE = REF_FILE_PY2_NUMERIC
else:
    REF_FILE_LEGACY = REF_FILE_PY3_LEGACY
    REF_FILE = REF_FILE_PY3_NUMERIC


class BaseTest(unittest.TestCase):

    VERBOSE = True

    def _enable_output(self):
        sys.stdout = sys.__stdout__

    def _disable_output(self):
        suppress_text = io.StringIO()
        sys.stdout = suppress_text

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls().VERBOSE:
            cls()._disable_output()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if not cls().VERBOSE:
            cls()._enable_output()

    def _find_last_output(self):

        def _file_is_recent(file, seconds=RECENT_FILE_S):
            file_time = os.path.getmtime(file)
            return (time.time() - file_time) < seconds

        max_dir = None
        max_file = None
        max_mtime = 0
        for dirname, subdirs, files in os.walk(PATH_OUT):
            for fname in files:
                if not fname.endswith(".out"):
                    continue
                full_path = os.path.join(dirname, fname)
                mtime = os.stat(full_path).st_mtime
                if mtime > max_mtime:
                    max_mtime = mtime
                    max_dir = dirname
                    max_file = fname

        found = max_dir+"/"+max_file
        if not _file_is_recent(found):
            raise Exception("File {} is too old, probably not from the last execution".format(found))
        return os.path.abspath(found)

    def run_pipeline_example(self, is_legacy=False):
        cmd = ""
        cmd += "cd {}; ".format(PATH_BASE)
        if is_legacy:
            cmd += "bash {}; ".format(PATH_EXAMPLE_LEGACY)
        else:
            cmd += "bash {}; ".format(PATH_EXAMPLE_NUMERIC)
        cmd += "cd {}".format(THIS_PATH)
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        stdout, stderr = process.communicate()

        if self.VERBOSE:
            if stdout:
                print("Stdout:")
                print(stdout)
            if stderr:
                print("Stderr:")
                print(stderr)
        return self._find_last_output()

    def run_pipeline_legacy_example(self):
        return self.run_pipeline_example(is_legacy=True)

    def compare_results(self, file_a, file_b):
        return get_error_indicator(file_a, file_b, force=False, path_src=PATH_SRC)

    def check_result_legacy(self, result):
        return self.compare_results(REF_FILE_LEGACY, result)

    def check_result(self, result):
        return self.compare_results(REF_FILE, result)
