from github import Github
from bs4 import BeautifulSoup
import urllib.request
import urllib
import sys

class Person:
  def __init__(self, issue, pr, user):
    self.issue = issue
    self.pr = pr
    self.user = user

if len(sys.argv) > 1:
    g = Github(sys.argv[1])
else:
    print("enter access code: ")
    g = Github(input())

if len(sys.argv) > 2:
    repoName = sys.argv[2]
else:
    print("enter repo name: ")
    repoName = input()

if len(sys.argv) > 3:
    projectName = sys.argv[3]
else:
    print("enter project name: ")
    projectName = input()

if len(sys.argv) > 4:
    columnName = sys.argv[4]
else:
    print("enter column name: ")
    columnName = input()

for repoItr in g.get_user().get_repos():
    if repoItr.name == repoName:
        repo = repoItr

print("using repo: " + repo.name)

for projectItr in repo.get_projects():
    if projectItr.name == projectName:
        project = projectItr

for columnItr in project.get_columns():
    if columnItr.name == columnName:
        column = columnItr

pRequests = list()

for cardItr in column.get_cards():
    if(hasattr(cardItr.get_content(), "pull_request")):
        pRequests.append(cardItr.get_content().as_pull_request())

entries = list()

for pRequest in pRequests:
    res = urllib.request.urlopen(pRequest.html_url).read()

    soup = BeautifulSoup(res, "html.parser")
    input = soup.select(".js-issue-sidebar-form > .my-1 > a")
    
    issues = [x["href"] for x in input]

    for issue in issues:
        entries.append(Person(issue, pRequest.html_url, pRequest.user.login))

output = ""

for entry in entries:
    output += entry.issue + "\t"
    output += entry.pr + "\t"
    output += entry.user + "\n"

f = open("output.txt", "w+", encoding="utf-8")
f.write(output)
f.close()