import pytest
from api_engine.api_engine import Books, BaseApi
from constants.constants import ProjectConstants
from helpers.checking_performer import CheckingPerformer, StatusCheck, CheckingBookAuthorPresenceInResponse


@pytest.mark.usefixtures('domain')

class TestClass:
    def test_3_check_the_book_author_presence_in_response(self, book_id_list):
        get_books = Books(self.server_url)
        BaseApi.add_simple_step(f'Get response for {ProjectConstants.BOOKS_ENDPOINT}')
        status, received_response = get_books.book_status_and_response()
        BaseApi.add_simple_step(f'Performing tests')
        test_results = CheckingPerformer([
            StatusCheck(status),
            CheckingBookAuthorPresenceInResponse(book_id_list)
        ]).execute()
        assert test_results == True