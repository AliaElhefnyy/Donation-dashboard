import pandas as pd

def load_data():
    donations = pd.read_csv("data/donations.csv", parse_dates=['date'])
    projects = pd.read_csv("data/projects.csv")
    volunteers = pd.read_csv("data/volunteers.csv")
    return donations, projects, volunteers
