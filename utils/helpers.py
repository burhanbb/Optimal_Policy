import numpy as np

class CallCenter:
    def __init__(self, T, M, L1, L2, M1, M2, DT):
        self.time_horizon = T
        self.max_calls = M
        self.arrival_rate_1 = L1
        self.arrival_rate_2 = L2
        self.service_rate_1 = M1
        self.service_rate_2 = M2
        self.time_step = DT
        self.V = np.full((int(T/DT) + 1, M + 1, M + 1, 2), np.inf)
        self.V[:, 0, 0, :] = 0

    def expected_cost(self, q1, q2, assign_to_rep1, customer_type):
        if customer_type == 0:
            if assign_to_rep1:
                return (q1 + 1) / self.service_rate_1 + q2 / self.service_rate_2
            else:
                return q1 / self.service_rate_1 + (q2 + 1) / self.service_rate_2
        elif customer_type == 1:
            return q1 / self.service_rate_1 + (q2 + 1) / 2

    def fetch_optimal_policy(self):
        for time_step in range(1, int(self.time_horizon / self.time_step) + 1):
            time_remaining = self.time_horizon - time_step * self.time_step
            for q1 in range(self.max_calls + 1):
                for q2 in range(self.max_calls + 1):
                    for customer_type in range(2):
                        if q1 + q2 > self.max_calls:
                            continue

                        cost_rep1 = self.expected_cost(q1, q2, True, customer_type=0)
                        cost_rep2 = self.expected_cost(q1, q2, False, customer_type=0)

                        if q1 + 1 <= self.max_calls:
                            self.V[time_step, q1 + 1, q2, 0] = min(self.V[time_step, q1 + 1, q2, 0], cost_rep1 + self.V[time_step - 1, q1, q2, 0])
                        if q2 + 1 <= self.max_calls:
                            self.V[time_step, q1, q2 + 1, 0] = min(self.V[time_step, q1, q2 + 1, 0], cost_rep2 + self.V[time_step - 1, q1, q2, 0])

                        cost_rep2 = self.expected_cost(q1, q2, False, customer_type=1)

                        if q2 + 1 <= self.max_calls:
                            self.V[time_step, q1, q2 + 1, 1] = min(self.V[time_step, q1, q2 + 1, 1], cost_rep2 + self.V[time_step - 1, q1, q2, 1])

    def optimal_assignment(self, t, q1, q2, customer_type):
        if t < 0 or q1 + q2 > self.max_calls:
            return None
        elif customer_type == 0 and self.V[t, q1 + 1, q2, 0] <= self.V[t, q1, q2 + 1, 0]:
            return "Assign to Rep 1"
        elif customer_type == 0 and self.V[t, q1 + 1, q2, 0] > self.V[t, q1, q2 + 1, 0]:
            return "Assign to Rep 2"
        elif customer_type == 1:
            return "Assign to Rep 2"