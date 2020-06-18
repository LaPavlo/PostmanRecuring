import pytest
from api_engine.api_engine import Books, BaseApi
from helpers.checking_performer import CheckingPerformer, StatusCheck, RequestResponseCompare


@pytest.mark.usefixtures('domain')

class TestClass:
    def test_6_update_book(self, create_book):
        book = Books(self.server_url)
        BaseApi.add_simple_step(f'Generate request body for {book.books_endpoint} to update book')
        book_to_update = book.create_book_data()
        BaseApi.add_simple_step(f'Update book: {create_book}')
        status, received_response = book.update_book(str(create_book), book_to_update)
        BaseApi.add_simple_step(f'Performing tests')
        test_results = CheckingPerformer([
            StatusCheck(status),
            RequestResponseCompare([[received_response, book_to_update]])
        ]).execute()
        assert test_results == True