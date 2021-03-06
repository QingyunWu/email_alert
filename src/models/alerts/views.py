from flask import Blueprint, request, render_template, session, redirect, url_for
from flask import make_response

from src.models.alerts.alert import Alert
from src.models.items.item import Item

__author__ = 'Qingyun Wu'

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
def create_alert():
	if request.method == 'POST':
		name = request.form['name']
		url = request.form['url']
		price_limit = float(request.form['price_limit'])
		#create the item before creating the alert
		item = Item(name, url)
		item.save_to_mongo()
		# session['email'] to get the user's email
		alert = Alert(session['email'], price_limit, item._id)
		alert.load_item_price()  # This already saves to MongoDB

	# What happens if it's a GET request
	return render_template("alerts/new_alert.html")  # Send the user an error if their login was invalid


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
def edit_alert(alert_id):
	if request.method == 'POST':
		price_limit = float(request.form['price_limit'])

		alert = Alert.find_by_id(alert_id)
		alert.price_limit = price_limit
		alert.load_item_price()  # This already saves to MongoDB

	# What happens if it's a GET request
	return render_template("alerts/edit_alert.html", alert=Alert.find_by_id(alert_id))  # Send the user an error if their login was invalid


@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
	Alert.find_by_id(alert_id).deactivate()
	return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
def activate_alert(alert_id):
	Alert.find_by_id(alert_id).activate()
	return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
	Alert.find_by_id(alert_id).delete()
	return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
def get_alert_page(alert_id):
	return render_template('alerts/alert.html', alert=Alert.find_by_id(alert_id))


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
	# send emails if there is a price match
	Alert.find_by_id(alert_id).load_item_price()
	Alert.find_by_id(alert_id).send_email_if_price_reached()
	# return redirect(url_for('.get_alert_page', alert_id=alert_id))
	return make_response(get_alert_page(alert_id=alert_id))