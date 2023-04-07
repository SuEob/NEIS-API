# from flask import Flask, render_template
import json
import school_api_test

if __name__ == "__main__" :
    
    school_info = {
        "office_of_education": "서울특별시교육청",
        "school": "가락고등학교"
    }

    school_api_test.get_info(**school_info)
    school_api_test.get_data()
    school_api_test.meal_service()


    with open("output.json", "w", encoding="utf-8") as file :
        json.dump(school_api_test.school_meal, file, indent=4, ensure_ascii=False)

#     print(params["param"]["CODE"])

#     app = Flask("JobScrapper")

#     @app.route("/")
#     def main():
#         return render_template("home.html", name="J.Seo")

#     app.run("127.0.0.1")
