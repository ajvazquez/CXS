from tests.base import BaseTest, REF_FILE_PY2_LEGACY, REF_FILE_PY3_LEGACY


class TestReference(BaseTest):

    VERBOSE = False
    SHOW_ERROR = True
    THRESHOLD_ERROR_PY2_PY3 = 10e-10

    def test_ref_py2_py3(self):
        acc_error = self.compare_results(REF_FILE_PY2_LEGACY, REF_FILE_PY3_LEGACY)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR_PY2_PY3)
