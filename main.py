import select
import socket
import time

import PlanewaveTCP

my_PW = PlanewaveTCP.PlanewaveTCP("127.0.0.1", 8877)

print(my_PW.GetStatus())
