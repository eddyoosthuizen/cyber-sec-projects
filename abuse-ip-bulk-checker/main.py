import argparse
import pandas as pd
import requests
import json

# Set up the argument parser
parser = argparse.ArgumentParser(description='Process IP addresses from a CSV file and write the JSON output to another CSV file.')
parser.add_argument('input_csv', type=str, help='The path to the input CSV file containing IP addresses')
parser.add_argument('output_csv', type=str, help='The path to the output CSV file to save the results')

# Parse the arguments
args = parser.parse_args()

# Read the input CSV file
input_df = pd.read_csv(args.input_csv, header=None)
input_df.columns = ['ipAddress']

# Prepare the output data
output_data = []

# Function to query the IP information
def query_ip(ip_address):
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {
        'Accept': 'application/json',
        'Key': '9fac0c95697885e45852b3730b6ac9060fadf8c0763f53b79384a5dc662065d8222d191184fb631e'  # Replace with your actual API key
    }
    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90'
    }
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data

# Process each IP address
for ip in input_df['ipAddress']:
    result = query_ip(ip)
    #print(result)
    ip_data = {
        'ipAddress': result.get('data', {}).get('ipAddress', None),
        'abuseConfidenceScore': result.get('data', {}).get('abuseConfidenceScore', None),
        'isTor': result.get('data', {}).get('isTor', None),
        'countryCode': result.get('data', {}).get('countryCode', None),
        'isp': result.get('data', {}).get('isp', None),
        'totalReports': result.get('data', {}).get('totalReports', None),
        # Add other fields as needed
    }
    output_data.append(ip_data)

# Create the output DataFrame
output_df = pd.DataFrame(output_data)

# Write the output DataFrame to a CSV file
output_df.to_csv(args.output_csv, index=False)

print(f"CSV file created and populated successfully at {args.output_csv}")

