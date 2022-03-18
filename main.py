import pandas as pd
from db.util import *
from geopy.distance import distance
import requests
import json
from tqdm import tqdm
import argparse


def ip_to_aws_server(ip_address, aws_map, use_token=True):
    """
    Given an IP address, find the closest AWS region (e.g. us-east-1). This is done using existing data about the
    latitude and longitude of AWS servers and the geopy package. If the IP address is invalid, we default to us-east-1
    :param use_token: Boolean flag indicating whether or not to use the ipinfo.io token from the .env file
    :param ip_address: The IP address to GeoLocate
    :param aws_map: A map of (lat, long) tuples to the corresponding AWS region names
    :return: The closest AWS region to the location of the IP address
    """
    # Find the latitude and longitude for this IP address
    if use_token:
        ip_info_token = os.getenv("IPINFO_TOKEN")
        ip_info = json.loads(requests.get(f"https://ipinfo.io/{ip_address}?token={ip_info_token}").text)
    else:
        ip_info = json.loads(requests.get(f"https://ipinfo.io/{ip_address}").text)
    if 'bogon' in ip_info or 'loc' not in ip_info:
        # This means that the IP address is invalid or we could not find the lat and long, so we default to us-east-1
        return 'us-east-1'
    lat, long = ip_info['loc'].split(',')
    # Calculate the distances from this IP to each of the AWS servers. Find the closest server and return it.
    region_distances = [(distance((lat, long), aws_geoloc).km, aws_code) for aws_geoloc, aws_code in aws_map.items()]
    closest_region = sorted(region_distances, key=lambda x: x[0])[0][1]  # Get the region with the minimum distance
    return closest_region


def main():
    # Parse the arguments for the --ignore_token flag
    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore_token', action='store_true', help='An optional flag to specify whether or not to'
                                                                    'ignore the ipinfo.io token from the .env file')
    args = parser.parse_args()
    use_token = not args.ignore_token

    print('Loading in CSV files (Extraction)...')
    df = pd.read_csv('DATA.csv')
    aws_df = pd.read_csv('datacenters.csv')

    print('Finding AWS regions for records (Transformation)...\n')
    # Create a map of (lat, long) tuples to AWS region names
    aws_map = dict()
    for idx, row in aws_df.iterrows():
        aws_map[(row['lat'], row['long'])] = row['aws-code']

    # For each record, find the closest AWS region based on the IP address
    for idx, ip_address in enumerate(tqdm(df['ip_address'])):
        df.at[idx, 'aws_server'] = ip_to_aws_server(ip_address, aws_map, use_token=use_token)

    print('Inserting records into database (Loading)...')
    bulk_insert(df, 'sfl_data')

    print('Done!')


if __name__ == '__main__':
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    main()
