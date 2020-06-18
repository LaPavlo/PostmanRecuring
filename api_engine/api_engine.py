from copy import deepcopy
from random import randint
import allure
from datetime import datetime
import requests
import json
from faker import Factory

from constants.constants import ProjectConstants


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

class Books(BaseApi):
    def __init__(self, domain):
        super().__init__(domain)
        self.redundant_keys = ['id']
        self.books_endpoint = ProjectConstants.BOOKS_ENDPOINT

    # def books_status_and_response(self):
    #     status, received_response = self.get_status_and_response(self.books_endpoint)
    #     return status, received_response
    # Можно переделать на одну функцию
    def book_status_and_response(self, id=""):
        status, received_response = self.get_status_and_response(self.books_endpoint  + "/" + id)
        return status, received_response

    def delete_book_and_get_status(self, id):
        status = self.delete_and_get_status(self.books_endpoint + "/" + id)
        return status

    def create_book_data(self):
        fake = Factory.create()
        title = fake.catch_phrase()
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



class Shops(BaseApi):
    def __init__(self, domain):
        super().__init__(domain)
        self.shops_endpoint = ProjectConstants.SHOPS_ENDPOINT

    def shops_status_and_response(self):
        status, received_response = self.get_status_and_response(self.shops_endpoint)
        return status, received_response