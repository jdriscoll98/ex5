from django.shortcuts import render
import csv

# Create your views here.
def home(request):
    return render(request, "app/home.html")


def us_cases(request):
    # read csv
    data = csv.DictReader(open("app/static/data/covid-data-10-16-20.csv"))
    total_cases, new_cases, labels = [], [], []
    for row in data:
        if row["iso_code"] == "USA":
            if row["total_cases"] and row["new_cases"]:
                total_cases.append(row["total_cases"])
                new_cases.append(row["new_cases"])
                labels.append(row["date"])

    return render(
        request,
        "app/us_cases.html",
        {
            "total_cases": total_cases,
            "new_cases": new_cases,
            "labels": labels,
        },
    )


def avg_cases_and_deaths(request):
    # read csv
    data = csv.DictReader(open("app/static/data/covid-data-10-16-20.csv"))
    countries = {}
    for row in data:
        if not countries.get(row["location"]):
            countries[row["location"]] = {
                "months": [
                    {
                        "total_new_cases": 0,
                        "total_deaths": 0,
                        "number_of_days": 0,
                    }
                ]
            }
        current_country = row["location"]
        current_month = int(row["date"][0]) - 1
        number_of_months = len(countries[current_country]["months"]) - 1
        if current_month >= number_of_months:
            countries[current_country]["months"].append(
                {
                    "total_new_cases": 0,
                    "total_deaths": 0,
                    "number_of_days": 0,
                    "month": current_month - 1,
                }
            )
        current_month_data = countries[current_country]["months"][current_month]
        current_month_data["total_new_cases"] += int(row["new_cases"])
        current_month_data["total_deaths"] += int(row["deaths"])
        current_month_data["number_of_days"] += 1
        countries[current_country]["months"][current_month] = current_month_data

    max_month_of_each_country = {}
    for country in countries:
        max_month_of_each_country[country] = max(
            countries[country]["months"],
            key=lambda x: x["total_new_cases"] / x["number_of_days"],
        )

    print(max_month_of_each_country)

    return render(
        request,
        "app/avg_cases_and_tests.html",
    )
