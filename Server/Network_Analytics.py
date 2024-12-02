import time
import pandas as pd
import os

def network_analytics_init(): # create csvs if they dont exist
    if not os.path.isfile('upload_stats.csv'):
        upload_stats_df = pd.DataFrame(columns=['username', 'file_name', 'file_size(MB)', 'upload_rate(MB/s)', 'transfer_time(s)', 'system_response_time(s)', 'timestamp'])
        upload_stats_df.to_csv('upload_stats.csv', index=False)
    if not os.path.isfile('download_stats.csv'):
        download_stats_df = pd.DataFrame(columns=['username', 'file_name', 'file_size(MB)', 'download_rate(MB/s)', 'transfer_time(s)', 'system_response_time(s)', 'timestamp'])
        download_stats_df.to_csv('download_stats.csv', index=False)


 # store upload stats
def save_upload_stats(username, file_name, file_size, upload_rate, transfer_time, system_response_time):
    upload_stats_df = pd.read_csv('upload_stats.csv')
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    upload_stats_df.loc[len(upload_stats_df)] = [username, file_name, file_size, upload_rate, transfer_time, system_response_time, timestamp]
    upload_stats_df.to_csv('upload_stats.csv', index=False)


# store download stats
def save_download_stats(username, file_name, file_size, download_rate, transfer_time, system_response_time):
    download_stats_df = pd.read_csv('download_stats.csv')
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    download_stats_df.loc[len(download_stats_df)] = [username, file_name, file_size, download_rate, transfer_time, system_response_time, timestamp]
    download_stats_df.to_csv('download_stats.csv', index=False)

