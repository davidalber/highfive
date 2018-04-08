from copy import deepcopy
from highfive.payload import Payload
from highfive.tests import base
import json
import mock
from nose.plugins.attrib import attr
import unittest

@attr(type='unit')
class TestPayload(base.BaseTest):
    @classmethod
    def setUpClass(cls):
        cls.open_pr_payload = json.loads(cls._load_fake('open-pr.payload'))
        cls.new_comment_payload = json.loads(
            cls._load_fake('create-comment.payload')
        )

    ###########################################################################
    # Testing is_fork for new PRs and comments.
    ###########################################################################
    def test_pr_repo_is_fork(self):
        payload = Payload(self.open_pr_payload)
        self.assertTrue(payload.repo.is_fork())

    def test_pr_repo_is_not_fork(self):
        payload = deepcopy(self.open_pr_payload)
        payload['repository']['fork'] = False
        payload = Payload(payload)
        self.assertFalse(payload.repo.is_fork())

    def test_comment_repo_is_fork(self):
        payload = Payload(self.new_comment_payload)
        self.assertTrue(payload.repo.is_fork())

    def test_comment_repo_is_not_fork(self):
        payload = deepcopy(self.new_comment_payload)
        payload['repository']['fork'] = False
        payload = Payload(payload)
        self.assertFalse(payload.repo.is_fork())

    ###########################################################################
    # Testing repository owner username for new PRs and comments.
    ###########################################################################
    def test_pr_repo_owner(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(payload.repo.owner, 'davidalber')

    def test_comment_repo_owner(self):
        payload = Payload(self.new_comment_payload)
        self.assertEqual(payload.repo.owner, 'rust-lang')

    ###########################################################################
    # Testing repository name for new PRs and comments.
    ###########################################################################
    def test_pr_repo_name(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(payload.repo.name, 'highfive')

    def test_comment_repo_name(self):
        payload = Payload(self.new_comment_payload)
        self.assertEqual(payload.repo.name, 'rust')

    ###########################################################################
    # Testing PR number.
    ###########################################################################
    def test_pr_number(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(payload.number, 1)

    def test_comment_pr_number(self):
        payload = Payload(self.new_comment_payload)
        self.assertEqual(payload.number, 1)

    ###################################
    ### Testing PR-only data fields ###
    ###################################
    def test_base_label(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(payload.pr.base.label, 'davidalber:master')

    def test_base_repo_owner(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(payload.pr.base.repo.owner, 'davidalber')

    def test_base_repo_name(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(payload.pr.base.repo.name, 'highfive')

    def test_pr_creator(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(payload.pr.creator, 'davidalber')

    def test_pr_url(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(
            payload.pr.url,
            'https://api.github.com/repos/davidalber/highfive/pulls/1'
        )

    def test_pr_body(self):
        payload = Payload(self.open_pr_payload)
        self.assertEqual(
            payload.pr.body,
            "I've created this to exercise an instance of highfive against this repository."
        )

    ########################################
    ### Testing comment-only data fields ###
    ########################################
    def test_issue_state(self):
        payload = Payload(self.new_comment_payload)
        self.assertEqual(payload.issue.state, 'open')

    def test_issue_is_pr_true(self):
        payload = Payload(self.new_comment_payload)
        self.assertTrue(payload.issue.is_pr())

    def test_issue_is_pr_false(self):
        payload = deepcopy(self.new_comment_payload)
        del(payload['issue']['pull_request'])
        payload = Payload(payload)
        self.assertFalse(payload.issue.is_pr())

    def test_issue_creator(self):
        payload = Payload(self.new_comment_payload)
        self.assertEqual(payload.issue.creator, 'davidalber')

    def test_issue_assignee(self):
        payload = Payload(self.new_comment_payload)
        self.assertEqual(payload.issue.assignee, None)

    def test_issue_assignee2(self):
        payload = deepcopy(self.new_comment_payload)
        payload['issue']['assignee'] = 'foouser'
        payload = Payload(payload)
        self.assertEqual(payload.issue.assignee, 'foouser')

    ###################################
    ### Testing comment data fields ###
    ###################################
    def test_commenter(self):
        payload = Payload(self.new_comment_payload)
        self.assertEqual(payload.comment.commenter, 'davidalber')

    def test_comment(self):
        payload = Payload(self.new_comment_payload)
        self.assertEqual(payload.comment.body, 'r? @davidalber')
