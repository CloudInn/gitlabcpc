# gitlabcpc
Gitlab Cross Projects commands


### Why?
Sometimes your sprint/milestone would involve working on more than one project across your gitlab installation. 
In that case you would need to create the same milestone on every project in gitlab, create the labels you might need
in every project, etc..

*Gitlabcpc* is a command line tool that allows you to perform these operations once and apply them on all projects.

### Features

1. Milestones creation
2. Labels creation
3. Branches creation, deletion, protection, unprotection and setting as default
4. Reporting (There are only three functional reports now: Estimated Hours per milestone, Time spent per milestone, Unestimated issues per milestone)


### Warning

Deleting branches is a dangerous operation, and it is very likely you won't need it. So use it with caution.

### TODO

* Add more reports
* Allow the operations to be applied on a selected list of projects not all of them
* Add more parameter options to the reports 

### Requirements

* python 3+
* Gitlab 8.8+

I only tested this against gitlab Community Edition but in theory 
the same code should work fine against the enterprise edition.

### Installation

```
pip install git+https://github.com/CloudInn/gitlabcpc.git
```

Once installed on the first run you'll need to provide the tool with your gitlab URL and your personal access token.
You can consult [Gitlab's documentation](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) on how to 
create a personal access token.

### Usage


* Milestones creation
```
pickle@rick:~/$ gitlabcpc milestones create
```

* Labels creation
```
pickle@rick:~/$ gitlabcpc labels create
```

* Branches operations
```
pickle@rick:~/$ gitlabcpc branches create
pickle@rick:~/$ gitlabcpc branches delete
pickle@rick:~/$ gitlabcpc branches protect
pickle@rick:~/$ gitlabcpc branches unprotect
pickle@rick:~/$ gitlabcpc branches set-default
```

* Generate report
```
pickle@rick:~/$ gitlabcpc reports generate --milestone-name="17.11"
```
