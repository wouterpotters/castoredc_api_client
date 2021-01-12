import pytest


@pytest.fixture(scope="class")
def item_totals(client):
    def return_item_totals(endpoint, base=False):
        return client.request_size(endpoint, base)

    return return_item_totals
