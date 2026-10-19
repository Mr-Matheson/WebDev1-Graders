from bs4 import BeautifulSoup
import requests
import re

# Function to grade an HTML test part 2 assignment
def grade_volunteer_form(url, student_name, assignment_name):
    feedback = []
    total_score = 0  # Maximum score based on rubric
    return total_score, feedback