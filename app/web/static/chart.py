import matplotlib.pyplot as plt
import pandas as pd

def generate_chart(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['time'], data['forecast'], label='Forecast')
    plt.plot(data['time'], data['real_time'], label='Real-Time Data')
    plt.plot(data['time'], data['past'], label='Past Predictions')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Prediction Chart')
    plt.grid(False)
    plt.savefig('app/web/static/chart.png')
    plt.close()