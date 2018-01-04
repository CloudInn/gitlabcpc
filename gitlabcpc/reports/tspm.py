"""Time spent per milestone

Count the total time spent for the issues in a milestone
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
#    @make_spin(Default, "Generating...")
    def generate(self):

        issues = []

        projects = {}


        for project in self.gitlab.projects.all(per_page=100):
            projects[project.id] = project.name
            for milestone in project.milestones.list(per_page=1000):
                if self.milestone_name and milestone.title == self.milestone_name:
                    issues = issues + milestone.issues(per_page=10000)

        data = {'total_spent': {'label': 'Total hours', "Hours": {'value': 0, 'formatter': 'seconds'}},
                'projects': {'label': 'Per project'},
                'engineers': {'label': 'Per Engineer'}}

        for issue in issues:
            issue_spent = issue.time_stats()['total_time_spent']
            data['total_spent']['Hours']['value'] += issue_spent
            if projects[issue.project_id] in data['projects']:
                data['projects'][projects[issue.project_id]]['value'] = data['projects'][projects[issue.project_id]]['value'] + issue_spent
            else:
                data['projects'][projects[issue.project_id]] = {'value': issue_spent, 'formatter': 'seconds' }

            if not issue.assignee:
                engineer = 'Unassigned'
            else:
                engineer = issue.assignee.name
            if engineer in data['engineers']:
                data['engineers'][engineer]['value'] = data['engineers'][engineer]['value'] + issue_spent
            else:
                data['engineers'][engineer] = {'value': issue_spent, 'formatter': 'seconds' }

        self.data = data
