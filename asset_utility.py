import os
import requests


SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
sheety_header = {"Authorization": f'Bearer {SHEETY_TOKEN}'}


class AssetUtility:
    def __init__(self):
        pass

    def all_assets(self):
        get_asset_url = 'https://api.sheety.co/e8a815d97433f8fe431090ac021cf9fc/24K/assets'
        response = requests.get(url=get_asset_url, headers=sheety_header)
        assets_json = response.json()
        assets = [asset for asset in assets_json['assets']]
        print(assets)
        return assets

    def assign_owner(self, asset_id, user_id):
        pass

    def unassign_owner(self, asset_id):
        pass
