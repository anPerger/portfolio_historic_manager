import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
import requests
import webbrowser
from threading import Timer
from bson.json_util import dumps, loads
import json
import pymongo
from pymongo import MongoClient



client = MongoClient()

portfolio_hist_db = client["portfolio_hist"]
hist_avgs_col = portfolio_hist_db["avgs"]

app = Flask(__name__)

@app.route("/return-historic-avgs", methods=["GET"])
def return_historic_avgs():

    stock_avgs = hist_avgs_col.find_one({"type": "stocks"})
    bond_avgs = hist_avgs_col.find_one({"type": "bonds"})
    inflation_avgs = hist_avgs_col.find_one({"type": "inflation"})

    del stock_avgs["_id"]
    del bond_avgs["_id"]
    del inflation_avgs["_id"]

    historic_averages = {"stocks": stock_avgs, "bonds": bond_avgs, "inflation": inflation_avgs}
    
    return jsonify({"results": historic_averages})

if __name__ == "__main__":
    app.run(port=8005, debug=True)