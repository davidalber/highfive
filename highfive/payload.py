class Payload(object):
    def __init__(self, payload):
        self.payload = payload

    @property
    def repo(self):
        return Repository(self.payload['repository'])

    @property
    def number(self):
        return self.payload.get('number') or self.payload['issue']['number']

    @property
    def pr(self):
        return PullRequest(self.payload['pull_request'])

    @property
    def issue(self):
        return Issue(self.payload['issue'])

    @property
    def comment(self):
        return Comment(self.payload['comment'])

class Repository(object):
    def __init__(self, payload):
        self.payload = payload

    def is_fork(self):
        return self.payload['fork']

    @property
    def owner(self):
        return self.payload['owner']['login']

    @property
    def name(self):
        return self.payload['name']

class PullRequest(object):
    def __init__(self, payload):
        self.payload = payload

    @property
    def base(self):
        return Branch(self.payload['base'])

    @property
    def creator(self):
        return self.payload['user']['login']

    @property
    def url(self):
        return self.payload['url']

    @property
    def body(self):
        return self.payload['body']

class Branch(object):
    def __init__(self, payload):
        self.payload = payload

    @property
    def label(self):
        return self.payload['label']

    @property
    def repo(self):
        return Repository(self.payload['repo'])

class Issue(object):
    def __init__(self, payload):
        self.payload = payload

    @property
    def state(self):
        return self.payload['state']

    def is_pr(self):
        return 'pull_request' in self.payload

    @property
    def creator(self):
        return self.payload['user']['login']

    @property
    def assignee(self):
        return self.payload['assignee']

class Comment(object):
    def __init__(self, payload):
        self.payload = payload

    @property
    def commenter(self):
        return self.payload['user']['login']

    @property
    def body(self):
        return self.payload['body']
