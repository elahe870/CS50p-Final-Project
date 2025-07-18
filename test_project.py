import pytest
import requests
from project import  extract_coin_ids, sort_cryptos_by_potential, calculate_score

from unittest.mock import patch


def test_extract_coin_ids():
    assert extract_coin_ids("solana,bitcoin") == ["solana", "bitcoin"]
    assert extract_coin_ids(" ripple ") == ["ripple"]

def test_sort_cryptos_by_potential():
    def fortest_get(url):
        class fortestresponse:
            def raise_for_status(self): pass
            def json(self):
                if "coin1" in url:
                    return {
                        'name': 'CoinOne',
                        'symbol': 'c1',
                        'market_data': {
                            'price_change_percentage_24h': 4,
                            'total_volume': {'usd': 5000000000},
                            'market_cap': {'usd': 2000000000},
                            'price_change_percentage_7d': 7
                        }
                    }
                elif "coin2" in url:
                    return {
                        'name': 'CoinTwo',
                        'symbol': 'c2',
                        'market_data': {
                            'price_change_percentage_24h': 7,
                            'total_volume': {'usd': 7000000000},
                            'market_cap': {'usd': 4000000000},
                            'price_change_percentage_7d': 11
                        }
                    }
        return fortestresponse()

    with patch("project.requests.get", side_effect=fortest_get):
        result = sort_cryptos_by_potential(["coin1", "coin2"])
        assert len(result) == 2
        assert result[0]["name"] == "CoinTwo"  # Higher score
        assert result[1]["name"] == "CoinOne"


def test_calculate_score():
    data = {
        'market_data': {
            'price_change_percentage_24h': 4,
            'total_volume': {'usd': 5000000000},
            'market_cap': {'usd': 2000000000},
            'price_change_percentage_7d': 7
        }
    }
    score = calculate_score(data)
    assert score>0



