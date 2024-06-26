from datetime import datetime

from lib.smartcontracts.SCInterface import SCInterface


class MockSC(SCInterface):

    commitments = None
    start_time = None
    upper_bounds = None
    coins = None
    solutions = None
    initial_timestamp = None

    def initiate(self, coins, start_time, extra_time, upper_bounds, helper_id):
        self.coins = coins
        self.start_time = start_time
        self.extra_time = extra_time
        self.upper_bounds = upper_bounds
        self.helper_id = helper_id
        self.commitments = []
        self.solutions = []
        self.initial_timestamp = int(datetime.now().timestamp())
        return self

    def add_solution(self, solution, witness):
        time = int(datetime.now().timestamp())
        self.solutions.append((solution, witness, time))
        return time

    def get_message_at(self, i):
        return self.solutions[i][0]

    def switch_to_account(self, account):
        pass
