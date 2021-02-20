from tests.base import BaseTest, REF_FILE_PY2_LEGACY, REF_FILE_PY3_LEGACY, REF_FILE_PY2_NUMERIC, REF_FILE_PY3_NUMERIC


class TestReference(BaseTest):

    VERBOSE = False
    SHOW_ERROR = True
    THRESHOLD_ERROR_PY2_PY3 = 10e-10

    def test_ref_py2_py3_legacy(self):
        """
        Compare legacy reference files py2-py3.
        """
        acc_error = self.compare_results(REF_FILE_PY2_LEGACY, REF_FILE_PY3_LEGACY)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR_PY2_PY3)

    def test_ref_py2_py3(self):
        """
        Compare numeric sorting reference files py2-py3.
        """
        acc_error = self.compare_results(REF_FILE_PY2_LEGACY, REF_FILE_PY3_LEGACY)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR_PY2_PY3)
