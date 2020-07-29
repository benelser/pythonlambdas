from bs4 import BeautifulSoup
from json import JSONEncoder
import requests, json

# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-venv

class Blog():
    def __init__(self, lead, date, title, href, imgsrc):
        self.Lead = lead
        self.Date = date
        self.Title = title
        self.Href = href
        self.ImageSource = imgsrc
        super().__init__()

    def to_string(self):
        return "Title: " + self.Title + "\n" + "Date: " + self.Date + "\n" + "Lead: " + self.Lead + "\n" + "HREF: " + self.Href + "\n" + "ImageSource: " + self.ImageSource + "\n" 

# subclass JSONEncoder
# https://pynative.com/make-python-class-json-serializable/
class BlogEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def lambda_handler(event, context):
    #Target web page
    root_url = "https://www.cartalk.com"
    url = "https://www.cartalk.com/blogs/latest"

    #Connection to web page
    response = requests.get(url)

    # # Convert the response HTLM string into a python string
    # html = response.text
    blogscollection = []

    # Create soup object from page source
    soup = BeautifulSoup(response.text, 'html.parser')

    # get specific div element searching on class name
        # https://stackoverflow.com/questions/2136267/beautiful-soup-and-extracting-a-div-and-its-contents-by-id
    firstblogdiv = soup.find("div", {"class" : "row attachment attachment-before"})
    lead = firstblogdiv.find("div", {"class" : "field-item even"}).text
    date = firstblogdiv.find("span", {"class": "date-display-single"}).text

    # getting child element under above element
    firstblogatag = firstblogdiv.find("a", {"class" : "link-dark"}, href=True)
    title = firstblogatag.find("img")['title']
    href = root_url + firstblogatag['href']
    imgsrc = firstblogatag.find("img")['src']


    # Add first blog to blogs array
    blogscollection.append(Blog(lead, date, title, href, imgsrc))

    # Get blog section element searching for class
    blogsgrid = soup.find("div", {"class" : "row mt-3"})
    blogs = blogsgrid.find_all("div", {"class" : "col-md-4 mb-2"})

    for blog in blogs:
        lead = blog.find("div", {"class" : "field-item even"}).text
        date = blog.find("span", {"class": "date-display-single"}).text

        # getting child element under above element
        blogatag = blog.find("a", {"class" : "link-dark"}, href=True)
        title = blogatag.find("img")['title']
        href = root_url + blogatag['href']
        imgsrc = blogatag.find("img")['src']
        blogscollection.append(Blog(lead, date, title, href, imgsrc))
    
    return {
        'statusCode': 200,
        'body': json.dumps(encodedblogs)
    }
