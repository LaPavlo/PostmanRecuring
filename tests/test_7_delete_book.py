import pytest
from api_engine.api_engine import Books, BaseApi
from helpers.checking_performer import CheckingPerformer, StatusCheck


@pytest.mark.usefixtures('domain')

class TestClass:
    def test_7_delete_book(self, create_book):
        delete_books = Books(self.server_url)
        BaseApi.add_simple_step(f'Delete book: {create_book}')
        status = delete_books.delete_book_and_get_status(str(create_book))
        BaseApi.add_simple_step(f'Performing tests')
        test_results = CheckingPerformer([
            StatusCheck(status)
        ]).execute()
        assert test_results == True