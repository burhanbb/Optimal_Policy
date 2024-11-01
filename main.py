from utils.helpers import CallCenter

EXIT = 1
while(EXIT == 1):
    print("\nWelcome to your Optimal Policy for Assigning Call Center Representative Program")

    # try:
    T = float(input("\nPlease enter time horizon:"))
    M = int(input("\nPlease enter Maximum number of calls in the system:"))
    L1 = float(input("\nPlease enter arrival rate of type 1 customers:"))
    L2 = float(input("\nPlease enter arrival rate of type 2 customers:"))
    M1 = float(input("\nPlease enter service rate of representative 1:"))
    M2 = float(input("\nPlease enter service rate of representative 2:"))
    DT = float(input("\nPlease enter time step:"))
    ST = float(input("\nPlease enter specific time step:"))
    Q1 = int(input("\nPlease enter current queue for representative 1:"))
    Q2 = int(input("\nPlease enter current queue for representative 2:"))
    CT = int(input("\nPlease enter type of customer (0 for type 1, 1 for type 2):"))

    call_object = CallCenter(T, M, L1, L2, M1, M2, DT, ST, Q1, Q2, CT)
    output_string = call_object.fetch_optimal_policy()
    print(f"\nAt time {T - ST*DT} with state (q1={Q1}, q2={Q2}, customer_type={CT}): Optimal action is to {output_string}")

    # except:
    #     print("\nIncorrect Input!")

    # finally:
    EXIT = int(input("\nDo you want to try again? (1 for Yes, 0 for No)"))