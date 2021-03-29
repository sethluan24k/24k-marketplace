import os
import requests

from collectible import Collectible


SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
sheety_header = {"Authorization": f'Bearer {SHEETY_TOKEN}'}


class CollectibleUtility:
    def __init__(self):
        self.collectibles = []
        self.all_collectibles()

    def all_collectibles(self):
        get_asset_url = 'https://api.sheety.co/e8a815d97433f8fe431090ac021cf9fc/24K/assets'
        response = requests.get(url=get_asset_url, headers=sheety_header)
        assets_json = response.json()
        print(assets_json)
        self.collectibles = [
            Collectible(asset['id'], asset['assetName'], asset['description'], asset['assetUrl'],
                        asset['thumbnail'], asset['price'], asset['ownerId']) for asset in assets_json['assets']
        ]

    def find_collectible(self, collectible_id):
        for collectible in self.collectibles:
            if collectible.collectible_id == collectible_id:
                return collectible
        return None

    def find_collectible_by_user(self, user_id):
        my_collection = [collectible for collectible in self.collectibles if collectible.owner_id == user_id]
        return my_collection

    def assign_owner(self, collectible_id, user_id):
        url = f'https://api.sheety.co/e8a815d97433f8fe431090ac021cf9fc/24K/assets/{collectible_id}'
        body = {
            'asset': {
                'ownerId': user_id
            }
        }
        requests.put(url=url, json=body, headers=sheety_header)
        # refresh
        self.all_collectibles()

    def unassign_owner(self, collectible_id):
        pass
