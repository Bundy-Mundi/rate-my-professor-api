from flask import Flask
from flask import request
from flask_cors import CORS
from rate_my_professor import CSULB
from bs4 import BeautifulSoup
import requests
import json

YEAR = 2022
BOX_CLASS = "indexList"
BY_SUBJECT = "By_Subject"
BY_COLLEGE = "By_College"
BY_GE = "By_GE_Requirement"
SET = {"subject":BY_SUBJECT, "college":BY_COLLEGE, "ge":BY_GE}

app = Flask(__name__)
CORS(app) 

@app.route("/")
def home_view():
        return "Hello World 2022"

@app.route("/spring")
def spring_view():
        filtered_result=[]
        c = CSULB()

        # Queries
        by = request.args.get("by")
        query = request.args.get("major")
        rating_limit = request.args.get("rating")

        if not by in SET:
                return json.dumps({"error": "Wrong args"})
        if by == "ge":
                # If sorted by GE, then change query to area
                query = request.args.get("area")
        if not query:
                return json.dumps({"error": "Wrong args"})
       
        url = f"http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_{YEAR}/{SET[by]}/{query}.html"
        x = c.search_professors_in_page(url)

        # Filters
        ## By Rating
        if rating_limit:
                if float(rating_limit) > 5: return json.dumps({"error": "Rating cannot be higher than 5.0"})
                for el in x:
                        if el["rating"] >= float(rating_limit):
                                filtered_result.append(el)
                return json.dumps(filtered_result)
        
        ## By upper & lower division
        ## By Course Code
        ## By Course Name
        ## By Prof Name

        return json.dumps(x)


@app.route("/fall")
def fall_view():
        url = f"http://web.csulb.edu/depts/enrollment/registration/class_schedule/Fall_{YEAR}/{SET[by]}/index.html"
        return url

@app.route("/spring/list")
def list_view():
        results = []
        big_lists = None
        url = f"http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_{YEAR}/"
        by = request.args.get("by")
        if not by: return json.dumps({"error":"Wrong args"})
        if not by in SET:
                return json.dumps({"error": "Wrong args"})

        url = f"{url}{SET[by]}/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        lists = soup.find(class_="indexList").find_all("li")
        for l in lists:
                item = l.find("a")
                code = item.attrs['href'].split('.')[0]
                results.append({"text": item.text, "code":code, "link": item.attrs['href']})
        return json.dumps(results)