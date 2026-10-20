from bs4 import BeautifulSoup
import requests
import re
import cssutils

# Function to grade an HTML test part 2 assignment
def grade_html_test_part_2(url, student_name, assignment_name):
    feedback = []
    total_score = 0  # Maximum score based on rubric

    try:
        # Fetch the website HTML with SSL verification disabled
        response = requests.get(url, verify=False)
        response.raise_for_status()
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')

        # Extract internal styles
        internal_styles = soup.find('style')
        internal_styles_content = internal_styles.text if internal_styles else ""

        def table_internal_styles_check(internal_style = ""):
            has_border = "border:" in internal_style
            has_bc = "border-collapse: collapse" in internal_style
            return has_border or has_bc
            

        def check_styles(tag):
            return tag.get('style') or table_internal_styles_check(internal_styles_content)

        # Task 1: Theme selection & page setup (8 pts)
        task_score = 8
        if not '<!DOCTYPE html>' in content and not '<!doctype html>' in content:
            feedback.append("Missing correct HTML5 doctype.")
            task_score -= 1
        if not soup.find('html'):
            feedback.append("Missing <html> element")
            task_score -= 1
        if not soup.find('head'):
            feedback.append("Missing <head> element")
            task_score -= 1
        if not soup.find('body'):
            feedback.append("Missing <body> element")
            task_score -= 1
        if not soup.find('meta', attrs={'name': 'author'}):
            feedback.append("Missing Author metadata")
            task_score -= 1
        if not soup.find('meta', attrs={'name': 'description'}):
            feedback.append("Missing Description metadata")
            task_score -= 1
        if not soup.find('meta', attrs={'name': 'keywords'}):
            feedback.append("Missing Keywords metadata")
            task_score -= 1
        if not soup.find('meta', attrs={'name': 'viewport'}):
            feedback.append("Missing Viewport metadata")
            task_score -= 1
        if not soup.find('meta', attrs={'charset': 'utf-8'}) and not soup.find('meta', attrs={'charset': 'UTF-8'}):
            feedback.append("Missing Charset metadata")
            task_score -= 1
        if not soup.find('title'):
            feedback.append("Missing title tag or it is incorrect.")
            task_score -= 1
        total_score += max(0, task_score)


        # Task 2: Heading with Hyperlinks (10 pts)
        task_score = 10
        headings = soup.find_all(['h1', 'h2', 'h3'])
        if not headings:
            feedback.append("Missing proper heading formatting (h1, h2, or h3).")
            task_score -= 5

        links = [a for a in soup.find_all('a', href=True) if a.get('target') == '_blank']
        if not links:
            feedback.append("Missing required hyperlinks that open in a new tab.")
            task_score -= 5
        elif len(links) < 2:
            feedback.append("Missing a required hyperlink that opens in a new tab.")
            task_score -= 2
        total_score += max(0, task_score)


        # Task 3: Styled Table with Content (12 pts)
        task_score = 12
        table = soup.find('table')
        if not table:
            feedback.append("Missing table.")
            task_score -= 12
        else:
            rows = table.find_all('tr')
            cells = table.find_all('td')
            headers = table.find_all('th')
            if len(rows) < 4:
                feedback.append("Table must have at least 4 rows.")
                task_score -= (4 - len(rows)) * 2  # Deduct 2 points per row missing
            if len(cells) + len(headers) < 12:
                feedback.append("Table must have at least 12 cells.")
                task_score -= 4
            if len(headers) < 3:
                feedback.append("Table missing proper amount of th tags")
                task_score -= 2
            if not check_styles(table):
                feedback.append("Table lacks necessary styling (inline or internal styles missing).")
                task_score -= 4
        total_score += max(0, task_score)
        

        # Task 4: Image with Styles (9 pts)
        task_score = 9
        image = soup.find('img')
        if not image:
            feedback.append("Missing image.")
            task_score -= 9
        elif not image.get('src'):
            feedback.append("Image source is missing.")
            task_score -= 9
        elif not check_styles(image):
            feedback.append("Image lacks required styling (inline or internal styles missing).")
            task_score -= 4
        total_score += max(0, task_score)


        # Task 5: Lists & Horizontal Rule (12 pts)
        task_score = 12

        ol_lists = soup.find_all('ol')
        ul_lists = soup.find_all('ul')
        if len(ol_lists) < 1 and len(ul_lists) < 1:
            feedback.append("Missing both required lists (one numbered and one bulleted list).")
            task_score -= 6
        elif len(ol_lists) < 1:
            feedback.append("Missing numbered list")
            task_score -= 2
        elif len(ul_lists) < 1:
            feedback.append("Missing bulleted list")
            task_score -= 2

        subheading_list = soup.find_all(re.compile(r"^h[2-6]$"))  # Find all H2-H6 tags
        heading_above_ordered_list = False
        heading_above_unordered_list = False
        for subheading in subheading_list:  # This look checks if each list has an h2-h6 tag directly in front of it
            next_tag = subheading.find_next_sibling()
            if next_tag and next_tag.name == "ol":
                heading_above_ordered_list = True
            elif next_tag and next_tag.name == "ul":
                heading_above_unordered_list = True

        if not heading_above_unordered_list and not heading_above_ordered_list:
            feedback.append("Missing subheadings above each list")
            task_score -= 4
        elif not heading_above_unordered_list or not heading_above_ordered_list:
            feedback.append("Missing a subheading above one of your lists")
            task_score -= 2

        hr = soup.find('hr')
        if not hr:
            feedback.append("Missing horizontal rule for content separation.")
            task_score -= 3
        total_score += max(0, task_score)


        # Task 6: Concluding Paragraph (6 pts)
        task_score = 6
        paragraphs = soup.find_all('p')
        long_paragraphs = [p for p in paragraphs if len(p.text.split()) >= 5]
        if not long_paragraphs:
            feedback.append("Concluding paragraph is missing or too short (must be at least 5 sentences).")
            task_score -= 6
        total_score += max(0, task_score)


        # Task 7: Final Touches (12 pts)
        task_score = 12
        special_char = re.search(r'&[#0-9a-zA-Z]+;', content) is not None
        if not special_char:
            feedback.append("Missing use of a special character entity (e.g., &copy;, &amp;).")
            task_score -= 6

        cssutils.log.setLevel("CRITICAL")  # Suppress nonessential cssutils warnings

        css_property_count = 0

        # Count the CSS properties across all inline styles
        internally_styled_elements = soup.find_all(style=True)
        for element in internally_styled_elements:
            inline_css = element['style']
            parsed_style = cssutils.parseStyle(inline_css)
            css_property_count += parsed_style.length

        if internal_styles:
            # Count the CSS properties across all internal style element
            rules = cssutils.parseString(internal_styles.text)
            for rule in rules:
                css_property_count += rule.style.length * len(rule.selectorText.split(",")) # Count properties multiple times for each selector if they're in a shared rule

        if css_property_count < 10:
            feedback.append("Missing at least 4 additional styles (inline or internal) to enhance the appearance.")
            task_score -= 6
        total_score += max(0, task_score)


        # Task 8: Overall organization & readability (6 pts)
        task_score = 6
        lines = content.split('\n')
        has_indentation = any(len(line) - len(line.lstrip()) > 0 for line in lines if line.strip())
        if not has_indentation:
            feedback.append("No indentation found in the file.")
            task_score -= 2
        total_score += max(0, task_score)

        

    except requests.exceptions.RequestException as e:
        feedback.append(f"Failed to fetch website: {e}~~")
        total_score = 0

    return total_score, feedback


if __name__ == "__main__":
    print(grade_html_test_part_2("http://smith.rhswebdev.com/CMVMPTN/html-test/", "", ""))