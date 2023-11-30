from flask import Blueprint

shop = Blueprint("shop", __name__, template_folder="shop_templates", url_prefix="/shop")

from . import routes