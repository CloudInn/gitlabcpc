"""Unestimated issues per milestone

List the issues that hasn't been estimated yet in the milestone.
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
                if self.milestone_name and milestone.title in self.milestone_name:
                    issues = issues + milestone.issues()
        data = {'total_issues': {'label': 'Total Issues', "Issues": {'value': 0}},
                'projects': {'label': 'Per project'}}
        for issue in issues:
            estimate = issue.time_stats()['time_estimate']
            if estimate == 0:
                data['total_issues']['Issues']['value'] +=  1
                if projects[issue.project_id] in data['projects']:
                    data['projects'][projects[issue.project_id]]['value'].append('#'+str(issue.iid)+": "+issue.title)
                else:
                    data['projects'][projects[issue.project_id]] = {'value': ['#'+str(issue.iid)+": "+issue.title]}
        self.data = data
