"""Base report, the class in this module will be inhirited by all reports.
Every report needs to gather its required parameters and set the output format.

"""

from prompts import *


__version__ = "0.1"


class BaseReport():
    only_active_milestones = True
    all_projects = True
    group_by_name = True
    gitlab = None
    milestone_name = None

    def __init__(self, gitlab, args):

        self.gitlab = gitlab
        self.milestone_name = args.milestone_name

    def get_params(self):
        """Get the report's parameters: milestone(s), all projects or group projects, etc.."""
        self.only_active_milestones = True if ReportMilestonesPrompt().input == 'yes' else False
        self.all_projects = True if ReportProjectsPrompt().input == 'all' else False

    def generate(self):
        """Make all the required API calls to return a dictionary containing the report results"""
        pass

    def render():
        """Render the generated results dictionary using the selected output method"""
        pass
