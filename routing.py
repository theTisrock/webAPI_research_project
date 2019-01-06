#
# ALL CODED BY CHRISTOPHER TOROK, EXCEPT WHERE INDICATED
#
from app_config import app
from flask import Flask, render_template, request, redirect
from YNAB_tool import *
from sms import get_txt_client

ynab = YNAB_tool()

@app.route("/")
def hello():
	return render_template("categories.html", categories_dict=ynab.get_budget_categoryids())

@app.route("/send", methods=['POST'])
def send_balances():
	cat_id_list = []

	if request.method == 'POST' and len(request.form) != 0:
		nm_id_dict = ynab.get_budget_categoryids()
		for x in range(0, len(nm_id_dict['name']) ):
			if nm_id_dict['name'][x] in request.form.keys():
				cat_id_list.append(str(nm_id_dict['name'][x]) + " $" + str(ynab.get_category_balance(request.form[nm_id_dict['name'][x]])/1000) )
				# the numeric data comes in the form of an integer and must be modified to a human readable dollar format.
				# to do this, the large integer is divided by 1000
		sms = get_txt_client()
		sms.messages.create(body=str(cat_id_list), from_='+18645010610', to='+18645094713')
		return render_template("sent.html", cat_bal=cat_id_list)
	return render_template("categories.html", categories_dict=ynab.get_budget_categoryids()) + "Please make a selection."

@app.route("/recent-transactions")
def show_last_10():
	recent_transactions = ynab.get_transactions_last10()

	for i in range(0, len(recent_transactions)):
		recent_transactions[i]['amount'] = recent_transactions[i]['amount']/1000
	return render_template("recent-transactions.html", recent_transactions=recent_transactions)

@app.route("/edit-transaction", methods=['POST'])
def show_edit_transaction():
	trans_data = ynab.get_transaction_data(request.form['id'])
	return render_template("edit-selection.html", trans_data=trans_data)

@app.route("/update-transaction", methods=['POST'])
def update_transaction():
	if request.method == 'POST' and len(request.form) != 0:
		id = request.form['id']
		amount_flt = float(request.form['update-amount'])*1000.0  # must convert amount back to integer that the YNAB api understands. times 1000, then cast to int
		amount = int(amount_flt)
		return ynab.update_transaction_amount(id, amount)
	return "No update"
