from flask import Flask
from flask import request, redirect, render_template
from flask import Response
from rate_my_professor import CSULB
from bs4 import BeautifulSoup
import requests
import json

YEAR = 2022
BOX_CLASS = "pageContent"
BY_SUBJECT = "By_Subject"
BY_COLLEGE = "By_College"
BY_GE = "By_GE_Requirement"
SET = {"subject":BY_SUBJECT, "college":BY_COLLEGE, "ge":BY_GE}
CLASS_SCHEDULE_BASE_URL = "http://web.csulb.edu/depts/enrollment/registration/class_schedule"

app = Flask(__name__)
response = Response()
response.headers["Access-Control-Allow-Origin"] = "*"
response.headers["Content-Type"] = "application/json"

def list_data(term, year, by):
        results = []
        url = f"{CLASS_SCHEDULE_BASE_URL}/{term.title()}_{year}/{SET[by]}/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        lists = soup.find(class_=BOX_CLASS).find_all("li")
        for l in lists:
                item = l.find("a")
                code = item.attrs['href'].split('.')[0]
                results.append({"text": item.text, "code":code, "link": item.attrs['href']})
        return results

@app.route("/")
def home_view():
        return render_template("index.html", home=True)

@app.route("/spring")
def spring_view():
        term = "spring"
        year = request.args.get("year")
        by = request.args.get("by")
        code = request.args.get("q")
        if not by in SET:
                return json.dumps({"error": "Wrong args"})
        if not by:
                return json.dumps({"error": "Wrong args"})
        if code:
                c = CSULB()
                url = f"{CLASS_SCHEDULE_BASE_URL}/{term.title()}_{YEAR}/{SET[by]}/{code}.html"
                data = c.search_professors_in_page(url)
                return render_template("index.html", data=data, term=term, year=year, by=by)
        return render_template("index.html", content=list_data(term, year, by), term=term, year=year, by=by)

@app.route("/fall")
def fall_view():
        term = "fall"
        year = request.args.get("year")
        by = request.args.get("by")
        code = request.args.get("q")
        if not by in SET:
                return json.dumps({"error": "Wrong args"})
        if not by:
                return json.dumps({"error": "Wrong args"})
        if code:
                c = CSULB()
                url = f"{CLASS_SCHEDULE_BASE_URL}/{term.title()}_{YEAR}/{SET[by]}/{code}.html"
                return render_template("index.html", data=c.search_professors_in_page(url), term=term, year=year, by=by)
        return render_template("index.html", content=list_data(term, year, by), term=term, year=year, by=by)
