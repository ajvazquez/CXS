import unittest
import subprocess
import os
import sys

from cx2d_lib import get_error_indicator


THIS_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_EXAMPLE = os.path.abspath(THIS_PATH+"/../../examples/run_example_vgos.sh")
PATH_BASE = os.path.abspath(THIS_PATH+"/../../")
PATH_OUT = THIS_PATH+"/../../output"
PATH_SRC = THIS_PATH+"/../../src"

EXAMPLES = THIS_PATH+"/../../examples/test_dataset_vgos/example_output/"


REF_FILE = EXAMPLES + "OUT_s0_v0.out"


class BaseTest(unittest.TestCase):

    VERBOSE = True

    def _enable_output(self):
        sys.stdout = sys.__stdout__

    def _disable_output(self):
        sys.stdout = open(os.devnull, 'w')

    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        if not self.VERBOSE:
            self._disable_output()

    def _find_last_output(self):
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
        return os.path.abspath(found)

    def run_pipeline_example(self):
        cmd = ""
        cmd += "cd {}; ".format(PATH_BASE)
        cmd += "bash {}; ".format(PATH_EXAMPLE)
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

    def check_result(self, result):
        return get_error_indicator(REF_FILE, result, force=False, path_src=PATH_SRC)
