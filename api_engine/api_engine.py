import allure
from datetime import datetime
import requests
import json
from faker import Factory

from constants.constants import ProjectConstants
from helpers.custom_exceptions import MethodNotFound

class BaseApi:

    def __init__(self, domain):
        self.domain = domain

    @staticmethod
    def return_formatted_current_date_and_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def add_simple_step(step_title):
        with allure.step(step_title):
            pass

    @allure.step("Send GET request to {endpoint} and return response and status")
    def get_status_and_response(self, endpoint):
        url_for_request = f'{self.domain}/{endpoint}'
        request_get = requests.get(url_for_request, auth=(ProjectConstants.LOGIN, ProjectConstants.PASSWORD))
        status = request_get.status_code
        received_response = request_get.json()
        request_headers = dict(request_get.request.headers)
        allure.attach(body=json.dumps(received_response, indent=4),
                      name=f'{self.return_formatted_current_date_and_time()}: Response of the {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(body=json.dumps(request_headers),
                      name=f'{self.return_formatted_current_date_and_time()}: Request headers of the {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        return status, received_response

    @allure.step("Send POST request to {endpoint} and return response and status")
    def post_and_get_status_and_response(self, endpoint, data):
        url_for_request = f'{self.domain}/{endpoint}'
        request_post = requests.post(url_for_request, auth=(ProjectConstants.LOGIN, ProjectConstants.PASSWORD), data=data)
        status = request_post.status_code
        received_response = request_post.json()
        request_headers = dict(request_post.request.headers)
        allure.attach(body=json.dumps(data, indent=4),
                      name=f'{self.return_formatted_current_date_and_time()}: Post request data to the {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(body=json.dumps(request_headers),
                      name=f'{self.return_formatted_current_date_and_time()}: Request headers of the {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(body=json.dumps(received_response, indent=4),
                      name=f'{self.return_formatted_current_date_and_time()}: Response after post {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        return status, received_response

    @allure.step("Send PUT request to {endpoint} and return response and status")
    def update_and_get_status_and_response(self, endpoint, data):
        url_for_request = f'{self.domain}/{endpoint}'
        request_post = requests.put(url_for_request, auth=(ProjectConstants.LOGIN, ProjectConstants.PASSWORD), data=data)
        status = request_post.status_code
        received_response = request_post.json()
        request_headers = dict(request_post.request.headers)
        allure.attach(body=json.dumps(data, indent=4),
                      name=f'{self.return_formatted_current_date_and_time()}: Update request data to the {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(body=json.dumps(request_headers),
                      name=f'{self.return_formatted_current_date_and_time()}: Request headers of the {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(body=json.dumps(received_response, indent=4),
                      name=f'{self.return_formatted_current_date_and_time()}: Response after updating {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        return status, received_response


    def delete_and_get_status(self, endpoint):
        endpoint = str(endpoint)
        url_for_request = f'{self.domain}/{endpoint}'
        request_delete = requests.delete(url_for_request, auth=(ProjectConstants.LOGIN, ProjectConstants.PASSWORD))
        status = request_delete.status_code
        request_headers = dict(request_delete.request.headers)
        allure.attach(body=json.dumps(request_headers),
                      name=f'{self.return_formatted_current_date_and_time()}: Request headers of the {endpoint}',
                      attachment_type=allure.attachment_type.JSON)
        return status

    @allure.step("Remove extra keys: {extra_keys}")
    def remove_extra_keys_from_response(self,  response, extra_keys):
        for i in extra_keys:
            response.pop(i, None)
        return response

    def execute_particular_http_method_to_list_return_statuses(self, endpoint, list_of_values, method):

        statuses_after_method_execution = []
        requested_method = self.method_factory(method)

        for i in list_of_values:
            final_endpoint = f'{endpoint}/{str(i)}'
            status = requested_method(final_endpoint)
            # Quick workaround since delete method doesn't return response.
            if requested_method == self.delete_and_get_status:
                dict_with_result = {final_endpoint: status}
            else:
                dict_with_result = {final_endpoint: status[0]}

            statuses_after_method_execution.append(dict_with_result)

        return statuses_after_method_execution


    def method_factory(self, method):

        if method == 'GET':
            return self.get_status_and_response
        elif method == 'POST':
            return self.post_and_get_status_and_response
        elif method == 'PUT':
            return self.update_and_get_status_and_response
        elif method == 'DELETE':
            return self.delete_and_get_status
        else:
            raise MethodNotFound




class Books(BaseApi):
    def __init__(self, domain):
        super().__init__(domain)
        self.redundant_keys = ['id']
        self.books_endpoint = ProjectConstants.BOOKS_ENDPOINT

    def book_status_and_response(self, id=""):
        status, received_response = self.get_status_and_response(self.books_endpoint  + "/" + id)
        return status, received_response

    def delete_book_and_get_status(self, id):
        status = self.delete_and_get_status(self.books_endpoint + "/" + id)
        return status

    def create_book_data(self):
        fake = Factory.create()
        title = "Beer and round asses"
        author = fake.name()
        rating = fake.year()
        year_published = fake.year()
        data = {
            "title": title,
            "author": author,
            "rating": rating,
            "year_published": year_published
        }
        return data

    def post_new_book(self, book):
        status, response = self.post_and_get_status_and_response(self.books_endpoint, book)
        received_response = self.remove_extra_keys_from_response(response, self.redundant_keys)
        return status, received_response

    def update_book(self, id, book):
        status, response = self.update_and_get_status_and_response(self.books_endpoint + "/" + id,
                                                                          data=book)
        received_response = self.remove_extra_keys_from_response(response, self.redundant_keys)
        return status, received_response

    def get_list_of_books_duplicates(self):
        status, received_response = self.book_status_and_response()
        temp = []
        duplicates = []
        for d in received_response :
            if d.get("title") not in temp :
                temp.append(d.get("title"))
            else :
                duplicates.append(d.get("id"))
        return duplicates

    def delete_list_of_books_return_statuses(self, list_of_books):

        if list_of_books:
            return self.execute_particular_http_method_to_list_return_statuses(self.books_endpoint,
                                                                               list_of_books,
                                                                               method='DELETE')
        else:
            return False

    def get_list_of_books_return_statuses(self, list_of_books):

        if list_of_books:
            return self.execute_particular_http_method_to_list_return_statuses(self.books_endpoint,
                                                                               list_of_books,
                                                                               method='GET')
        else:
            return False




class Shops(BaseApi):
    def __init__(self, domain):
        super().__init__(domain)
        self.shops_endpoint = ProjectConstants.SHOPS_ENDPOINT

    def shops_status_and_response(self):
        status, received_response = self.get_status_and_response(self.shops_endpoint)
        return status, received_response