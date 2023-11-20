import logging, functools


class Logger:
    def __init__(self, name, log_file, level=logging.INFO):
        """Function setup as many loggers as you want"""

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)

    def log_function_call(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(
                f"Calling function {func.__name__} with arguments {args} and keyword arguments {kwargs}"
            )
            try:
                result = func(*args, **kwargs)
                self.logger.info(f"Function {func.__name__} completed successfully")
                return result
            except Exception as e:
                self.logger.error(f"Function {func.__name__} raised an error: {str(e)}")
                raise e  # re-raise the caught exception after logging it

        return wrapper

    def class_log(self, cls):
        for name, method in cls.__dict__.items():
            if callable(method):
                setattr(cls, name, self.log_function_call(method))
        return cls
