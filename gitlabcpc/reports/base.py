"""Base report, the class in this module will be inhirited by all reports.
Every report needs to gather its required parameters and set the output format.

"""

from prompts import *
import csv
import datetime
import importlib

__version__ = "0.1"


class BaseReport():
    only_active_milestones = True
    all_projects = True
    group_by_name = True
    gitlab = None
    milestone_name = None
    data = None
    output = None

    def __init__(self, gitlab, args):

        self.gitlab = gitlab
        self.milestone_name = args.milestone_name
        if args.output:
            self.output = args.output

    def get_params(self):
        """Get the report's parameters: milestone(s), all projects or group projects, etc.."""
        self.only_active_milestones = True if ReportMilestonesPrompt().input == 'yes' else False
        self.all_projects = True if ReportProjectsPrompt().input == 'all' else False

    def generate(self):
        """Make all the required API calls to return a dictionary containing the report results"""
        pass

    def render(self):
        """Render the generated results dictionary using the selected output method"""
        if not self.output:
            now = datetime.datetime.now()
            self.output = self.__module__[8:]+'-'+now.isoformat()
        with open(self.output+".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                     quotechar=',', quoting=csv.QUOTE_MINIMAL)
            for key in self.data:
                if 'label' in self.data[key]:
                    label = self.data[key].pop('label')
                writer.writerow([label])
                for head in self.data[key]:
                    if 'formatter' in self.data[key][head]:
                        formatter = getattr(importlib.import_module("misc"), "format_"+self.data[key][head]['formatter'])
                        writer.writerow(['', head, formatter(self.data[key][head]['value'])])
                    else:
                        if isinstance(self.data[key][head]['value'], list):
                            writer.writerow(['', '', head])
                            for item in self.data[key][head]['value']:
                                writer.writerow(['', '', '', item])
                        else:
                            writer.writerow(['', head, self.data[key][head]['value']])


        print("Report saved at: %s.csv" %self.output)
