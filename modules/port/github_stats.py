#!/usr/bin/env python
"""
github_stats.py - casca Github Info Module
Copyright 2009-2015, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

Developed by kaneda (http://jbegleiter.com / https://github.com/kaneda)

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
"""

import json
import random
import re
import traceback
import urllib2
import urlparse

# For information about the Github API check out https://developer.github.com/v3/

BASE_URL = "https://api.github.com"
DEFAULT_HEADER = { "Accept": "application/vnd.github.v3+json" }

def fetch_github(casca, url, term):
    t = urllib2.quote(term)
    if '%' in term:
        t = urllib.quote(term.replace('%', ''))

    request = urllib2.Request(url % t, headers=DEFAULT_HEADER)

    try:
        content = json.loads(urllib2.urlopen(request).read())
        return content
    except Exception as e:
        casca.say("An error occurred fetching information from Github: {0}".format(e))
        return None

# Search for repos
def github_search(casca, term):
    search_url = BASE_URL + "/search/repositories?q=%s"

    content = fetch_github(casca, search_url, term)
    if content is None: return

    if "items" in content:
        # Take no more than 5 entries
        list_names = min(len(content["items"]), 5)
        full_names = ", ".join([ x["full_name"] for x in content["items"][:5] ])
        casca.say("Top {0} results: {1}".format(list_names, full_names))
    else:
        casca.say("Couldn't find any repos matching your search term")

# Search for users
def github_user_search(casca, term):
    search_url = BASE_URL + "/search/users?q=%s"

    content = fetch_github(casca, search_url, term)
    if content is None: return

    if "items" in content:
        # Take no more than 5 entries
        list_names = min(len(content["items"]), 5)
        logins = ", ".join([ x["login"] for x in content["items"][:5] ])
        casca.say("Top {0} results: {1}".format(list_names, logins))
    else:
        casca.say("Couldn't find any users matching your search term")

# List open PRs
def github_prs(casca, project):
    pr_url = BASE_URL + "/repos/%s/pulls"

    content = fetch_github(casca, pr_url, project)
    if content is None: return

    num_pulls = len(content)

    casca.say("{0} has {1} open PRs".format(project, num_pulls))
    if num_pulls > 0:
        list_pulls = min(num_pulls, 5)
        titles = ", ".join([ x["title"] for x in content[:5] ])
        casca.say("Latest {0} PRs: {1}".format(list_pulls, titles))

# User info
def github_user(casca, login):
    user_url = BASE_URL + "/users/%s"

    content = fetch_github(casca, user_url, login)
    if content is None: return

    if "login" not in content:
      msg = "An error occurred fetching user info"
      if "message" in content:
        msg += ": {0}".format(content["message"])
      casca.say(msg)
      return

    user_info = "Login: {0}; Member since: {1}; Name: {2}; Public repos: {3}; Followers: {4}".format(content["login"], content["created_at"], content["name"], content["public_repos"], content["followers"])
    if "company" in content and len(content["company"]) > 0:
      user_info += "; Company: {0}".format(content["company"])

    if "blog" in content and len(content["blog"]) > 0:
      user_info += "; Blog: {0}".format(content["blog"])

    if "location" in content and len(content["location"]) > 0:
      user_info += "; Location: {0}".format(content["location"])

    if "hireable" in content and content["hireable"] is not None:
      user_info += "; Available for hire: {0}".format(content["hireable"])

    casca.say(user_info)

# Contributors to a repo
def github_contribs(casca, project):
    contrib_url = BASE_URL + "/repos/%s/contributors"

    content = fetch_github(casca, contrib_url, project)
    if content is None: return

    num_contribs = len(content)

    casca.say("This repo has {0} contributors".format(num_contribs))
    if num_contribs > 0:
        list_contribs = min(num_contribs, 5)
        contribs = ", ".join([ "{0} ({1} contributions)".format(x["login"], x["contributions"]) for x in content[:5] ])
        casca.say("Top {0} contributors: {1}".format(list_contribs, contribs))

# Jenni commands start here
def gh_search(casca, input):
    origterm = input.groups()[1]
    if not origterm:
        return casca.say('Perhaps you meant ".github_search repo"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_search(casca, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_search.commands = ['gh_search', 'github_search', 'gh_s', 'gh']
gh_search.priority = 'low'
gh_search.rate = 10

def gh_user_search(casca, input):
    origterm = input.groups()[1]
    if not origterm:
        return casca.say('Perhaps you meant ".github_user_search user"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_user_search(casca, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_user_search.commands = ['gh_user_search', 'github_user_search', 'gh_usr_s']
gh_user_search.priority = 'low'
gh_user_search.rate = 10

def gh_user_info(casca, input):
    origterm = input.groups()[1]
    if not origterm:
        return casca.say('Perhaps you meant ".github_user_info user"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_user(casca, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_user_info.commands = ['gh_user_info', 'github_user_info', 'gh_usr', 'gh_user', 'gh_u']
gh_user_info.priority = 'low'
gh_user_info.rate = 10

def gh_prs(casca, input):
    origterm = input.groups()[1]
    if not origterm:
        return casca.say('Perhaps you meant ".github_prs user/repo"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_prs(casca, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_prs.commands = ['gh_prs', 'github_prs']
gh_prs.priority = 'low'
gh_prs.rate = 10

def gh_contribs(casca, input):
    origterm = input.groups()[1]
    if not origterm:
        return casca.say('Perhaps you meant ".github_contribs user/repo"?')
    origterm = origterm.encode('utf-8')
    origterm = origterm.strip()

    error = None

    try:
        result = github_contribs(casca, origterm)
    except IOError:
        error = "An error occurred connecting to Github"
        traceback.print_exc()
    except Exception as e:
        error = "An unknown error occurred: " + str(e)
        traceback.print_exc()
gh_contribs.commands = ['gh_contribs', 'github_contribs']
gh_contribs.priority = 'low'
gh_contribs.rate = 10

if __name__ == '__main__':
    print __doc__.strip()
