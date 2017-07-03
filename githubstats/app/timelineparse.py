import subprocess
import sys

def process(raw, jq):
    cmd = subprocess.Popen(jq,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           stdin=subprocess.PIPE,
                           shell=False,
                           bufsize=0)

    stdout, stderr = cmd.communicate(raw)
    for line in stdout.decode('utf-8').split("\n"):
        yield line

def issues(raw):
    jq = ['jq', '-c',
          '[ .[] | select( .type | contains("IssuesEvent"))] | .[] | { \
           "repo": .repo.name, \
           "action": .payload.action, \
           "time": .created_at, \
           "target": .payload.issue.title, \
           "message": .payload.issue.title \
           }']

    for line in process(raw, jq):
        yield line

def issuecomments(raw):
    jq = ['jq', '-c', 
          '[ .[] | select( .type | contains("IssueCommentEvent"))] | .[] | { \
          "repo": .repo.name, \
          "action": "issue comment", \
          "time": .created_at, \
          "target": .payload.issue.title, \
          "message": .payload.comment.body \
          }']

    for line in process(raw, jq):
        yield line

def pullrequest(raw):
    jq = ['jq', '-c', '[ .[] | select( .type | contains("PullRequestEvent"))] | .[] | { \
        "time": .created_at, \
        "repo": .repo.name, \
        "action": .payload.action, \
        "target": .payload.pull_request.title, \
        "message": .payload.pull_request.body \
        }']

    for line in process(raw, jq):
        yield line

def push(raw):
    jq = ['jq', '-c', '[ .[] | select( .type | contains("PushEvent"))] | .[] | { \
        "time": .created_at, \
        "repo": .repo.name, \
        "action": "push", \
        "target": "commit", \
        "message": .payload.commits[].message \
        }']

    for line in process(raw, jq):
        yield line

def create(raw):
    jq = ['jq', '-c', '[ .[] | select( .type | contains("CreateEvent"))] | .[] | { \
        "time": .created_at, \
        "repo": .repo.name, \
        "action": "create", \
        "target": .payload.ref_type, \
        "message": .payload.ref \
        }']

    for line in process(raw, jq):
        yield line

def watch(raw):
    jq = ['jq', '-c', '[ .[] | select( .type | contains("WatchEvent"))] | .[] | { \
        "time": .created_at, \
        "repo": .repo.name, \
        "action": "watch", \
        "target": "timeline", \
        "message": .payload.action \
        }']
    
    for line in process(raw, jq):
        yield line
    
def parse(data):
    for line in issues(data):
        yield line

    for line in issuecomments(data):
        yield line

    for line in push(data):
        yield line

    for line in create(data):
        yield line


