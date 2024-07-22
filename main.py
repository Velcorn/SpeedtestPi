import subprocess
import pandas as pd
import os
import datetime
import json

# Path to save speed test results
file_path = '/home/velcorn/SpeedtestPi/results.csv'


# Initialize the speed test
def run_speedtest():
    result = subprocess.run(['speedtest', '--format', 'json'], capture_output=True, text=True)
    return json.loads(result.stdout)


# Save results to a CSV file
def save_to_csv(data, file_path):
    df = pd.DataFrame([data])
    # Convert down/up to Mb/s, limit to timestamp, ping, jitter, download, upload, and jitter columns and round
    df['download'] = df['download'] / 125000
    df['upload'] = df['upload'] / 125000
    df = df[['timestamp', 'ping', 'ping_jitter', 'download', 'download_jitter', 'upload', 'upload_jitter']].round(0)
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)


# Main function to run speed test and save results
def main():
    try:
        results = run_speedtest()
        results = {
            'timestamp': datetime.datetime.now().replace(microsecond=0),
            'ping': results['ping']['latency'],
            'ping_jitter': results['ping']['jitter'],
            'download': results['download']['bandwidth'],
            'download_jitter': results['download']['latency']['jitter'],
            'upload': results['upload']['bandwidth'],
            'upload_jitter': results['upload']['latency']['jitter']
        }
        save_to_csv(results, file_path)
        print('Speed test completed successfully.')
    except Exception as e:
        print(f'Error running speed test: {e}')


if __name__ == '__main__':
    main()
