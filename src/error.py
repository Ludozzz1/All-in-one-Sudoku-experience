#classify to classify errors. Has a message and the time at which the error occured.

class InsertionError:
    def __init__(self, message, error_start):
        self.message = message
        self.error_start = error_start

    