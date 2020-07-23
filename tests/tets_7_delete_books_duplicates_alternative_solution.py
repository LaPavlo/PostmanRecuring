import pytest
from api_engine.api_engine import Books, BaseApi
from helpers.checking_performer import CheckingPerformer, StatusCheck, RequestResponseCompare


@pytest.mark.usefixtures('domain')

class TestClass:

    def test_7_after_deleting_duplicates_they_shouldnt_be_returned_by_server(self):

        books = Books(self.server_url)
        duplicates = books.get_list_of_books_duplicates()
        if duplicates:
            BaseApi.add_simple_step(f'Delete duplicates of books: {duplicates}')
            deleting_duplicates = books.delete_list_of_books_return_statuses(duplicates)
            get_deleted_books = books.get_list_of_books_return_statuses(duplicates)
            test_results_deleting = CheckingPerformer([StatusCheck(deleting_duplicates)]).execute()
            test_result_get_deleted_books = CheckingPerformer([StatusCheck(get_deleted_books, expected_status=404
                                                                           )]).execute()
            assert test_results_deleting is True
            assert test_result_get_deleted_books is True
        else:
            BaseApi.add_simple_step('No duplicates found')
            pytest.skip('No duplicates found')


