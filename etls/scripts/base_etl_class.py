import abc

class ETL(abc.ABC):


    @abc.abstractmethod
    def __call__(self):
        pass