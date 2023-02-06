from io import StringIO
from sys import stderr, stdout
from typing import TextIO


class Logger:
    INFO = "[\033[32mINFO\033[0m]:\t"
    ERROR = "[\033[31mERROR\033[0m]:\t"
    WARNING = "[\033[33mWARNING\033[0m]:\t"
    DEBUG = "[\033[35mDEBUG\033[0m]:\t"

    # volontary sep to "" to avoid space between *values

    @staticmethod
    def _capture(
        *values: object,
        sep: str,
        end: str,
        file: TextIO,
        flush: bool,
    ) -> str:
        output = StringIO()
        print(*values, sep=sep, end=end, file=output, flush=True)
        ret = output.getvalue()
        output.close()
        print(ret, end='', file=file, flush=flush)
        return ret

    @staticmethod
    def info(
        *values: object,
        sep: str = "",
        end: str = "\n",
        file: TextIO = stdout,
        flush: bool = True,
    ) -> str:
        return Logger._capture(
            Logger.INFO,
            *values,
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )

    @staticmethod
    def error(
        *values: object,
        sep: str = "",
        end: str = "\n",
        file: TextIO = stderr,
        flush: bool = True,
    ):
        return Logger._capture(
            Logger.ERROR,
            *values,
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )

    @staticmethod
    def warn(
        *values: object,
        sep: str = "",
        end: str = "\n",
        file: TextIO = stderr,
        flush: bool = True,
    ):
        return Logger._capture(
            Logger.WARNING,
            *values,
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )

    @staticmethod
    def debug(
        *values: object,
        sep: str = "",
        end: str = "\n",
        file: TextIO = stderr,
        flush: bool = True,
    ):
        return Logger._capture(
            Logger.DEBUG,
            *values,
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )

    @staticmethod
    def success(
        *values: object,
        sep: str = "",
        end: str = "\n",
        file: TextIO = stdout,
        flush: bool = True,
    ):
        return Logger._capture(
            "\033[32;1m",
            *values,
            "\033[0m",
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )

    @staticmethod
    def fail(
        *values: object,
        sep: str = "",
        end: str = "\n",
        file: TextIO = stdout,
        flush: bool = True,
    ):
        return Logger._capture(
            "\033[31;1m",
            *values,
            "\033[0m",
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )
