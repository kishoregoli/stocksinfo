import datetime
import os
import subprocess


curr_dir = os.path.dirname(__file__)

return_value = subprocess.call("python " + os.path.join(curr_dir, "nse_daily_data.py --day {}".format(datetime.datetime.now().date() - datetime.timedelta(1))))
if return_value == 0:
    subprocess.call("python " + os.path.join(curr_dir, "stocks_gist.py --day {}".format(
        datetime.datetime.now().date() - datetime.timedelta(1))))

