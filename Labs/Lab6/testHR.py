
import max30102
import hrcalc
import time


m = max30102.MAX30102()

dataHR=[]
time.sleep(5)   # Wait 5 seconds to place finger on the sensor.
for i in range(5):

    red, ir = m.read_sequential()

    dataHR[i*100:(i+1)*100] = red    # For raw data capturing. Not required!
    hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir[:100], red[:100])  # Calculating heart rate and SpO2 values from raw data.

    print(hr, hr_valid, spo2, spo2_valid)

