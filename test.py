
from datetime import datetime
dt_string = "[29/Nov/2017:19:22:12"
dt_object1 = datetime.strptime(dt_string, "[%d/%b/%Y:%H:%M:%S")
print("dt_object1 =", dt_object1)