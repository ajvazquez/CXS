from tests.base import BaseTest


class TestDev(BaseTest):

    VERBOSE = False
    SHOW_ERROR = False
    THRESHOLD_ERROR = 10e-20

    def test_pipeline_correlation_legacy_src_sources(self):
        """
        Pipeline correlation, legacy sorting, src symlinks.
        """

        num_out_pre = self.count_output_files()
        result = self.run_pipeline_legacy_src_example()
        num_out_post = self.count_output_files()

        self.assertTrue(num_out_pre < num_out_post)

        acc_error = self.check_result_legacy(result)

        if self.SHOW_ERROR:
            self._enable_output()
            print("Error for {}: {}".format(result, acc_error))
            self._disable_output()

        self.assertTrue(acc_error is not None)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR)

    def test_pipeline_correlation_legacy(self):
        """
        Pipeline correlation, legacy sorting.
        """

        num_out_pre = self.count_output_files()
        result = self.run_pipeline_legacy_example()
        num_out_post = self.count_output_files()

        self.assertTrue(num_out_pre < num_out_post)
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

        num_out_pre = self.count_output_files()
        result = self.run_pipeline_example()
        num_out_post = self.count_output_files()

        self.assertTrue(num_out_pre < num_out_post)
        acc_error = self.check_result(result)

        if self.SHOW_ERROR:
            self._enable_output()
            print("Error for {}: {}".format(result, acc_error))
            self._disable_output()

        self.assertTrue(acc_error is not None)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR)

    def test_spark_correlation(self):
        """
        Spark correlation.
        """

        num_out_pre = self.count_output_files()
        result = self.run_spark_example()
        num_out_post = self.count_output_files()

        self.assertTrue(num_out_pre < num_out_post)

        acc_error = self.check_result(result)

        if self.SHOW_ERROR:
            self._enable_output()
            print("Error for {}: {}".format(result, acc_error))
            self._disable_output()

        self.assertTrue(acc_error is not None)
        self.assertTrue(acc_error < self.THRESHOLD_ERROR)
