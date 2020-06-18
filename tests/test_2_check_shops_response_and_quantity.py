import pytest
from api_engine.api_engine import Shops, BaseApi
from constants.constants import ProjectConstants
from helpers.checking_performer import CheckingPerformer, StatusCheck, LengthCompare

@pytest.mark.usefixtures('domain')

class TestClass:
    def test_2_check_shop_response_code_and_quantity(self):
        get_shops = Shops(self.server_url)
        BaseApi.add_simple_step(f'Get response for {ProjectConstants.SHOPS_ENDPOINT}')
        status, received_response = get_shops.shops_status_and_response()
        BaseApi.add_simple_step(f'Performing tests')
        test_results = CheckingPerformer([
            StatusCheck(status),
            LengthCompare(received_response, ProjectConstants.SHOPS_DEFAULT_AMOUNT)
        ]).execute()
        assert test_results == True