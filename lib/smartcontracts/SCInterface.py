from abc import ABC, abstractmethod

class SCInterface(ABC):

    @abstractmethod
    def initiate(self, coins, start_time, extra_time, upper_bounds, helper_id):
        pass

    @abstractmethod
    def add_solution(self, solution, witness):
        pass

    @abstractmethod
    def get_message_at(self, i):
        pass

    @property
    @abstractmethod
    def upper_bounds(self):
        pass

    @upper_bounds.setter
    @abstractmethod
    def upper_bounds(self, upper_bounds):
        pass

    @property
    @abstractmethod
    def coins(self):
        pass

    @coins.setter
    @abstractmethod
    def coins(self, upper_bounds):
        pass

    @property
    @abstractmethod
    def start_time(self):
        pass

    @start_time.setter
    @abstractmethod
    def start_time(self, start_time):
        pass

    @property
    @abstractmethod
    def commitments(self):
        pass

    @commitments.setter
    @abstractmethod
    def commitments(self, commitments):
        pass

    @property
    @abstractmethod
    def solutions(self):
        pass

    @property
    @abstractmethod
    def initial_timestamp(self):
        pass
