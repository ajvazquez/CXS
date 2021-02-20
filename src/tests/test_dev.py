from tests.base import BaseTest


class TestReference(BaseTest):

    VERBOSE = False
    SHOW_ERROR = False
    THRESHOLD_ERROR = 10e-20

    def test_pipeline_correlation_legacy(self):
        """
        Pipeline correlation, legacy sorting.
        """

        result = self.run_pipeline_legacy_example()
        acc_error = self.check_result_legacy(result)

        if self.SHOW_ERROR:
            self._enable_output()
            print("Error for {}: {}".format(result, acc_error))
            self._disable_output()

        self.assertTrue(acc_error is not None)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR)

    def test_pipeline_correlation(self):
        """
        Pipeline correlation, numeric sorting.
        """

        result = self.run_pipeline_example()
        acc_error = self.check_result(result)

        if self.SHOW_ERROR:
            self._enable_output()
            print("Error for {}: {}".format(result, acc_error))
            self._disable_output()

        self.assertTrue(acc_error is not None)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR)
