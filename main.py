import PlanewaveTCP

my_PW = PlanewaveTCP.PlanewaveTCP("127.0.0.1", 8220)

print(my_PW.GetStatus())
