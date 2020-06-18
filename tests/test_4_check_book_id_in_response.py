import pytest
from api_engine.api_engine import Books, BaseApi
from helpers.checking_performer import CheckingPerformer, StatusCheck, CheckingIdInResponse


@pytest.mark.usefixtures('domain')

class TestClass:
    def test_4_check_book_id_in_response(self, create_book):
        get_books = Books(self.server_url)
        BaseApi.add_simple_step(f'Get response for book id = {create_book}')
        status, received_response = get_books.book_status_and_response(create_book)
        BaseApi.add_simple_step(f'Performing tests')
        test_results = CheckingPerformer([
            StatusCheck(status),
            CheckingIdInResponse(received_response, create_book)
        ]).execute()
        assert test_results == True

