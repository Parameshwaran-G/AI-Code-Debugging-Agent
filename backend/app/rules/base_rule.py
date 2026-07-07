from abc import ABC, abstractmethod


class BaseRule(ABC):

    @abstractmethod
    def check(self, parser_result):
        """
        Analyze the parsed source code.

        Returns:
            list[Finding]
        """
        pass