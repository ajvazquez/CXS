from tests.base import BaseTest


class TestReference(BaseTest):

    VERBOSE = False
    SHOW_ERROR = True
    THRESHOLD_ERROR = 10e-20

    def test_pipeline_correlation(self):

        result = self.run_pipeline_example()
        acc_error = self.check_result(result)

        if self.SHOW_ERROR:
            self._enable_output()
            print("Error for {}: {}".format(result, acc_error))

        self.assertTrue(acc_error is not None)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR)
