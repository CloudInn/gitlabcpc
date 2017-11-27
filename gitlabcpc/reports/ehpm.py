"""Estimated hours per milestone

Count the total hours estimated for the issues in a milestone
"""

from misc import *
from .base import BaseReport
from prompts import ReportMilestoneNamePrompt
from pyspin.spin import make_spin, Default

__version__ = "0.1"

class Report(BaseReport):

    def get_params(self):
        if not self.milestone_name:
            self.milestone_name = ReportMilestoneNamePrompt().input
    @make_spin(Default, "Generating...")
    def generate(self):

        issues = []

        projects = {}

        for project in self.gitlab.projects.all(per_page=100):
            projects[project.id] = project.name
            for milestone in project.milestones.list():
                if self.milestone_name and milestone.title == self.milestone_name:
                    issues = issues + milestone.issues()

        data = {'total_estimate': {'label': 'Total hours', "Hours": {'value': 0, 'formatter': 'seconds'}},
                'projects': {'label': 'Per project'},
                'engineers': {'label': 'Per Engineer'}}

        for issue in issues:
            issue_estimate = issue.time_stats()['time_estimate']
            data['total_estimate']['Hours']['value'] += issue_estimate
            if projects[issue.project_id] in data['projects']:
                data['projects'][projects[issue.project_id]]['value'] = data['projects'][projects[issue.project_id]]['value'] + issue_estimate
            else:
                data['projects'][projects[issue.project_id]] = {'value': issue_estimate, 'formatter': 'seconds' }

            if issue.assignee.username in data['engineers']:
                data['engineers'][issue.assignee.username]['value'] = data['engineers'][issue.assignee.username]['value'] + issue_estimate
            else:
                data['engineers'][issue.assignee.username] = {'value': issue_estimate, 'formatter': 'seconds' }

        self.data = data
