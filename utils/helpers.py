import numpy as np

class CallCenter:
    def __init__(self, T, M, lambda1, lambda2, mu1, mu2, dt, t, q1, q2, customer_type):
        self.time_horizon = T
        self.max_calls = M
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.service_rate_1 = mu1
        self.service_rate_2 = mu2
        self.time_step = dt
        self.specific_time_step = t 
        self.queue_1 = q1
        self.queue_2 = q2
        self.customer_type = customer_type
        self.V = np.full((int(T/dt)+1, M+1, M+1, 2), np.inf)
        self.V[:, 0, 0, :] = 0

    def expected_cost(self, q1, q2, assign_to_rep1, customer_type):
        if customer_type == 0:
            if assign_to_rep1:
                return (q1+1)/self.service_rate_1 + q2/self.service_rate_2
            else:
                return q1/self.service_rate_1 + (q2+1)/self.service_rate_2
        elif customer_type == 1:
            return q1/self.service_rate_1 + (q2+1)/2
        
    def optimal_assignment(self, t, q1, q2, customer_type):
        if t < 0 or q1 + q2 > self.max_calls:
            return "No valid assignment"
        elif customer_type == 0 and self.V[t, q1 + 1, q2, 0] <= self.V[t, q1, q2 + 1, 0]:
            return "Assign to Rep 1"
        elif customer_type == 0 and self.V[t, q1 + 1, q2, 0] > self.V[t, q1, q2 + 1, 0]:
            return "Assign to Rep 2"
        elif customer_type == 1:
            return "Assign to Rep 2"
        
    def fetch_optimal_policy(self):
        for time_step in range(1, int(self.time_horizon/self.time_step) + 1):
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

        optimal_action = self.optimal_assignment(self.specific_time_step, self.queue_1, self.queue_2, self.customer_type)