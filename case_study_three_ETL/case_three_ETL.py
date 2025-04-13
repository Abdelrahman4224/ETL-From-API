import requests
import pandas as pd

api_key = 'pk_860d4549b9663aaf8242ca20ba714d97cb'
base_url = 'https://a.klaviyo.com/api/'

headers = {
    'Authorization': f'Klaviyo-API-Key {api_key}',
    'Accept': 'application/json',
    'Revision': '2023-07-15'  
}

def fetch_data(endpoint, params=None):
    url = f'{base_url}{endpoint}/'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch {endpoint}: {response.status_code} - {response.text}')
        return None


def process_and_export(data, filename, fields):
    if data:
        data_list = []
        for item in data['data']:
            attributes = item.get('attributes', {})
            data_list.append({field: attributes.get(field, 'N/A') for field in fields})
        
        df = pd.DataFrame(data_list)
        df.to_csv(filename, index=False)
        print(f"Exported {filename}")

# campaigns
campaigns_params = {'filter': "equals(messages.channel,'email')"}
campaigns_data = fetch_data('campaigns', campaigns_params)
process_and_export(campaigns_data, 'campaigns.csv', [
    'name', 'status', 'archived', 'created_at', 'scheduled_at', 'updated_at', 'send_time'
])

# lists
lists_data = fetch_data('lists')
process_and_export(lists_data, 'lists.csv', ['name', 'created', 'updated', 'opt_in_process'])

# metrics
metrics_data = fetch_data('metrics')
process_and_export(metrics_data, 'metrics.csv', [
    'name', 'created', 'updated', 'integration'
])

# segments
segments_data = fetch_data('segments')
process_and_export(segments_data, 'segments.csv', [
    'name', 'definition', 'created', 'updated', 'is_active', 'is_processing', 'is_starred'
])

# profiles
profiles_data = fetch_data('profiles')
process_and_export(profiles_data, 'profiles.csv', [
    'email', 'phone_number', 'external_id', 'first_name', 'last_name', 'organization',
    'locale', 'title', 'created', 'updated', 'last_event_date', 'location'
])