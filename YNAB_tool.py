#
#
#
# ALL CODED BY CHRISTOPHER TOROK
#
#
#
#
import requests
import json

class YNAB_tool():
    """docstring for YNAB_obj"""
    
    def __init__(self):
        self.ynab_api_key = "your ynab api key goes here"
        self.base_url = "https://api.youneedabudget.com/v1"
        
    def get_budget_ids_list(self):
        base_url = self.base_url
        access_token = self.ynab_api_key

        resource = "/budgets"
        access_string = "?access_token=" + access_token

        uri = base_url + resource + access_string
        http_response = requests.get(uri)
        json_raw = http_response.text
        json_dict = http_response.json()

        num_budgets = len(json_dict['data']['budgets'])
        budget_list = []
        for index in range(0, num_budgets):
            budget_list.append(json_dict['data']['budgets'][index]['id'])
        # print(json_raw)
        return budget_list

    def get_budget_categoryids(self, budgetID="last-used"):
        """https://api.youneedabudget.com/v1/budgets/{budgetid}?access_token={ynab_api_key}"""
        base_url = self.base_url
        access_token = self.ynab_api_key

        parent = "/budgets"
        resource = f"/{budgetID}"
        access_string = f"?access_token={access_token}"
        uri = base_url + parent + resource + access_string

        http_response = requests.get(uri)

        json_raw = http_response.text
        json_list = requests.get(uri).json()['data']['budget']['categories']

        category_attribute = {'name': [], 'category_id': []}

        for x in range(0,len(json_list)):  # load names
            if json_list[x]['deleted'] is False:
                category_attribute['name'].append(json_list[x]['name'])
                category_attribute['category_id'].append(json_list[x]['id'])

        return category_attribute  # returns a dict with 3 keys mapped to 1 list each.

    def get_category_balance(self, categoryID, budgetID="last-used"):
        """https://api.youneedabudget.com/v1/budgets/{budgetID}/categories/{categoryid}?access_token={ynab_api_key}"""
        base_url = self.base_url
        access_token = self.ynab_api_key

        # get uri pieces
        budget_parent = "/budgets"
        budget_id = "/" + budgetID
        category_parent = "/categories"
        categoryid = f"/{categoryID}"
        access_string = f"?access_token={access_token}"

        # build uri
        uri = base_url + budget_parent + budget_id + category_parent + categoryid + access_string

        #  make a request
        response = requests.get(uri)

        # get data from request
        json_raw = response.text  # raw json text helpful for using a json parsing tool for visualization
        json_dict = response.json()
        # balance = json_dict['balance']
        category_balance = json_dict['data']['category']['balance']

        # pick out the balance for the given category id
        return category_balance  # return balance

    def get_transactions(self, budgetId="last-used"):
        base_url = self.base_url
        access_token = self.ynab_api_key

        resource="/budgets"
        budgetID = f"/{budgetId}"
        trans_resource = "/transactions"
        access_string = f"?access_token={access_token}"

        uri = base_url + resource + budgetID + trans_resource + access_string

        response = requests.get(uri)

        json_raw = response.text
        json_dict = response.json()
        trsnxn_list = json_dict['data']['transactions']

        return trsnxn_list

    def get_transactions_last10(self, budgetId="last-used"):
        trans_list = self.get_transactions(budgetId)

        total_txn_count = len(trans_list)
        start_index = total_txn_count - 10
        last10 = []

        for x in range(start_index, total_txn_count):
            last10.append(trans_list[x])

        return last10

    def get_transaction_ids_last10(self, budgetId="last-used"):
        trans_list = self.get_transactions(budgetId)

        total_txn_count = len(trans_list)
        start_index = total_txn_count - 10
        last10_ids = []

        for x in range(start_index, total_txn_count):
            last10_ids.append(trans_list[x]['id'])

        return last10_ids

    def get_transaction_data(self, trans_id, budgetID="last-used"):
        base_url = self.base_url
        budgets = "/budgets"
        budgetID = "/" + budgetID
        transactions = "/transactions" 
        transaction_id = "/" + trans_id
        access_string = f"?access_token={self.ynab_api_key}"

        uri = base_url + budgets + budgetID + transactions + transaction_id + access_string
        response = requests.get(uri)
        # json_raw = response.text
        json_dict = response.json()

        transaction_dict = json_dict['data']['transaction']

        return transaction_dict

    def update_transaction_amount(self, trans_id, amount, budgetID="last-used"):
        """/budgets/{budget_id}/transactions/{transaction_id} Updates an existing transaction"""
        base_url = self.base_url
        access_token = self.ynab_api_key

        budgets = "/budgets"
        budgetID = "/"+budgetID
        transactions = "/transactions"
        transaction_id = f"/{trans_id}"
        headers = {'Authorization' : f'Bearer {access_token}', 'Content-Type' : 'application/json'}

        uri = base_url + budgets + budgetID + transactions + transaction_id

        data = self.get_transaction_data(trans_id)

        data['amount'] = amount

        update = json.dumps({'transaction': data })

        return requests.put(uri, data=update, headers=headers).text
        
