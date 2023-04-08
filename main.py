# from flask import Flask, render_template
import json
import school_api

if __name__ == "__main__" :
    
    school_info = {
        "office_of_education": "서울특별시교육청",
        "school": "가재울고등학교"
    }
    school_api.get_info(**school_info)
    school_api.get_data()
    school_api.meal_service()
    school_api.time_table_service()

    with open("output_of_meal.json", "w", encoding="utf-8") as file :
        json.dump(school_api.school_meal, file, indent=4, ensure_ascii=False)

    with open("output_of_time.json", "w", encoding="utf-8") as file :
        json.dump(school_api.time_table, file, indent=4, ensure_ascii=False)        

#     app = Flask("JobScrapper")

#     @app.route("/")
#     def main():
#         return render_template("home.html", name="J.Seo")

#     app.run("127.0.0.1")
