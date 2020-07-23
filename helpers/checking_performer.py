from deepdiff import DeepDiff
from constants.constants import ProjectConstants
import jsonschema

class BaseChecker(object):
    pass

class SchemaCheck(BaseChecker):
    def __init__(self, response_for_schema, schema):
        self.response_for_schema = response_for_schema
        self.schema = schema

    def execute(self):
        schema_check_list = []
        request_jsons = self.response_for_schema
        schema = self.schema
        if isinstance(request_jsons, list):
            for i in request_jsons:
                schema_result = self.schema_check(i, schema)
                schema_check_list.append(schema_result)
        else:
            schema_result = self.schema_check(request_jsons, schema)
            schema_check_list.append(schema_result)

        what_the_result = list(set(schema_check_list))
        if what_the_result[0] == None and len(what_the_result)==1:
            schema_result = True
        else:
            error = ""
            for i in schema_check_list:
                error += i
            schema_result = error
        return schema_result

    def schema_check(self, request_jsons, schema):

        try:
            schema_check = jsonschema.Draft3Validator(schema).validate(request_jsons)
        except jsonschema.ValidationError as e:
            schema_check = str(e)
        return schema_check


class StatusCheck(BaseChecker):
    def __init__(self, status_to_check, expected_status=200):

        self.status_to_check = status_to_check
        self.expected_status = expected_status

    def compare_status_with_expected(self, status_to_check, expected_status, endpoint = None):

        if status_to_check == expected_status:
            return True
        else:
            if not endpoint:
                return ("Actual endpoint status {} is not equal to expected status {}"
                        .format(status_to_check, self.expected_status))
            else:
                return ("Actual {} status {} is not equal to expected status {}"
                        .format(endpoint, status_to_check, self.expected_status))


    def execute(self):
        if isinstance(self.status_to_check, list) or isinstance(self.status_to_check, tuple):
            status_check_result_string = ""
            for status in self.status_to_check:
                for k,v in status.items():
                    status_check_result = self.compare_status_with_expected(v, self.expected_status, k)
                    if status_check_result is not True:
                        status_check_result_string = status_check_result_string + f'\n {status_check_result}'
            if len(status_check_result_string):
                return status_check_result_string
            else:
                return True
        return self.compare_status_with_expected(self.status_to_check, self.expected_status)

class CheckingBookAuthorPresenceInResponse(BaseChecker):
    def __init__(self, response_items):
        self.response_items = response_items

    def execute(self):
        if len(self.response_items) > 0:
            return True
        else:
            return "No books of this author was found"

class CheckingIdInResponse(BaseChecker):
    def __init__(self, response_id, expected_id):
        self.response_id = response_id
        self.expected_id = expected_id
    def execute(self):
        if self.response_id.get("id") == self.expected_id:
            return True
        else:
            return f'Response is {self.response_id.get("id")}. Request is {self.expected_id}'

class LengthCompare(BaseChecker):

    def __init__(self, data_to_check, expected_length):

        self.len_of_data_to_check = len(data_to_check)
        self.expected_length = expected_length

    def execute(self):
        if self.len_of_data_to_check == self.expected_length:
            return True
        else:
            return(f"Actual length is {self.len_of_data_to_check} while expected is {self.expected_length}")

class RequestResponseCompare(BaseChecker):
    def __init__(self, request_response_to_compare, additional_text=None, ignore_order_value=True):
        self.request_response_to_compare = request_response_to_compare
        self.additional_text = additional_text
        self.ignore_order_value = ignore_order_value


    def execute(self):
        value_to_check = self.request_response_to_compare
        result = ""
        for i in range(len(value_to_check)):
            value_one = value_to_check[i][0]
            value_two = value_to_check[i][1]
            difference = str(DeepDiff(value_one, value_two, ignore_order=self.ignore_order_value))
            if difference == '{}': #this means that there are no difference
                continue
            else:
                result = result + self.additional_text[i] + difference if self.additional_text \
                    else result + ProjectConstants.DEFAULT_TEST_NAME_FOR_COMPARE_RESPONSE + difference
        if result == "":
            result = True
        return result

class CheckingPerformer():
    def __init__(self, tests_to_execute):
        self.tests_to_execute = tests_to_execute

    def add(self, test_to_execute):
        self.tests_to_execute.append(test_to_execute)

    def execute(self):
        checking_results = self.run()
        what_the_result = list(set(checking_results))
        if what_the_result[0] == True and len(what_the_result) == 1:
            checking_results = True
        # In case if there are other then True results for checking_result, then all errors would be concatenated into
        # a single one
        else:
            error = ""
            checking_results = list(filter(lambda x: x != True, checking_results))
            for i in checking_results:
                error += i
            checking_results = error

        return checking_results


    def run(self):
        checking_results = []
        for i in self.tests_to_execute:
            result = i.execute()
            checking_results.append(result)
        return checking_results