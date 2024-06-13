import pandas
import requests
import json

# Replace these with your TVDB API credentials
TVDB_API_KEY = 'API_KEY'
TVDB_API_URL = 'https://api4.thetvdb.com/v4'

def get_tvdb_token():
    url = f"{TVDB_API_URL}/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "apikey": TVDB_API_KEY
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 401:
        raise Exception("Unauthorized: Check your API key")
    response.raise_for_status()
    return response.json()['data']['token']

def get_tvdb_id(series_name, token):
    url = f"{TVDB_API_URL}/search?query={series_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        raise Exception("Unauthorized: Token may be expired or invalid")
    response.raise_for_status()
    search_results = response.json()
    if search_results['data']:
        return search_results['data'][0]['tvdb_id']
    return None

def main():
    try:
        # Read the Excel file
        df = pandas.read_excel('series_list.xlsx')

        # Assuming the series names are in the first column
        series_names = df.iloc[:, 0].tolist()

        # Authenticate and get the token
        token = get_tvdb_token()

        # List to hold the results
        results = []

        for series in series_names:
            tvdb_id = get_tvdb_id(series, token)
            if tvdb_id:
                results.append({"tvdbId": str(tvdb_id)})

        # Write the results to a JSON file
        with open('tvdb_ids.json', 'w') as json_file:
            json.dump(results, json_file, indent=2)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
