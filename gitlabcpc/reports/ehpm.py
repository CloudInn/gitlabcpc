"""Estimated hours per milestone

Count the total hours estimated for the issues in a milestone
"""

from .base import BaseReport

__version__ = "0.1"


class Report(BaseReport):

    def generate(self):

        issues = []

        projects = {}

        for project in self.gitlab.projects.all(per_page=100):
            projects[project.id] = project.name
            for milestone in project.milestones.list():
                if self.milestone_name and milestone.title == self.milestone_name:
                    issues = issues + milestone.issues()

        data = {'total_estimate': {'label': 'Total hours', 'total': 0},
                'projects': {'label': 'Per project'},
                'engineers': {'label': 'Per Engineer'}}

        for issue in issues:
            issue_estimate = issue.time_stats()['time_estimate']
            data['total_estimate']['total'] += issue_estimate
            if projects[issue.project_id] in data['projects']:
                data['projects'][projects[issue.project_id]]['total'] = data['projects'][projects[issue.project_id]]['total'] + issue_estimate
            else:
                data['projects'][projects[issue.project_id]] = {'total': issue_estimate }

            if issue.assignee.username in data['engineers']:
                data['engineers'][issue.assignee.username]['total'] = data['engineers'][issue.assignee.username]['total'] + issue_estimate
            else:
                data['engineers'][issue.assignee.username] = {'total': issue_estimate }

        self.data = data
