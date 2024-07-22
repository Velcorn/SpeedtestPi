import speedtest
import pandas as pd
import os
import datetime

# Path to save speed test results
file_path = 'speedtest_results.csv'


# Initialize the speed test
def run_speedtest():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    return st.results.dict()


# Save results to a CSV file
def save_to_csv(data, file_path):
    df = pd.DataFrame([data])
    # Convert down/up to Mb/s, limit to timestamp, ping, download, and upload columns and round to 0 decimal places
    df['download'] = df['download'] / 1e6
    df['upload'] = df['upload'] / 1e6
    df = df[['timestamp', 'ping', 'download', 'upload']].round(0)
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)


# Main function to run speed test and save results
def main():
    results = run_speedtest()
    # Add datetime rounded to seconds
    results['timestamp'] = datetime.datetime.now().replace(microsecond=0)
    save_to_csv(results, file_path)


if __name__ == '__main__':
    main()
