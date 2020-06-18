import pytest
from api_engine.api_engine import Books, BaseApi
from helpers.checking_performer import CheckingPerformer, StatusCheck
from constants.constants import ProjectConstants

@pytest.mark.usefixtures('domain')

class TestClass:
    def test_1_check_book_response_code(self):
        get_books = Books(self.server_url)
        BaseApi.add_simple_step(f'Get response for {ProjectConstants.BOOKS_ENDPOINT}')
        status, received_response = get_books.book_status_and_response()
        BaseApi.add_simple_step(f'Performing tests')
        test_results = CheckingPerformer([
            StatusCheck(status)
        ]).execute()
        assert test_results == True