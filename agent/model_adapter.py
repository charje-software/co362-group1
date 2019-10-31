from statsmodels.tsa.ar_model import ARResults


class Model:

    def __init__(self, model_file_name):
        self.saved_model = ARResults.load(model_file_name)
        self.test_amt = 1489    # last month's readings
        self.train_amt = 38237  # len(data) - test_amt

    def make_prediction(self, n):
        """ Uses saved model to make consumption prediction n steps ahead. """
        predictions = self.saved_model.predict(start=self.train_amt,
                                               end=self.train_amt+n-1,
                                               dynamic=False)
        pred = predictions[n-1]
        return pred
