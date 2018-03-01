"""Cement custom prompts

This module contains all the custom Cement prompts we'll use for all of our subcommands

"""

from cement.utils.shell import Prompt
from datetime import datetime

class GitlabcpcBasePrompt(Prompt):
    class Meta:
        options_separator = '|'
        max_attempts = 99

class MilestonesCreationDescriptionPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Enter the milestone description:"
        default = " "

    def process_input(self):
        if self.input == '':
            print("No description was entered")

class MilestonesCreationConfirmationPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Are you sure you wanna create a milestone with those parameters? This action can not be undone"
        options = ['yes', 'no']
        default = 'no'

class DatePrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Enter the date (in the format: YYYY-mm-dd):"
        label = ""
        date_format = "YYYY-mm-dd"
        default = " "

    def process_input(self):
        try:
            self.input = datetime.strptime(self.input.lower() , '%Y-%m-%d')
        except:
            print("You entered an invalid format, %s ignored" % self.Meta.label)
            self.input = ''

class MilestonesCreationStartDatePrompt(DatePrompt):
    class Meta:
        text = "Enter the milestone start date in the format %s:" % DatePrompt.Meta.date_format
        label = "start date"

class MilestonesCreationDueDatePrompt(DatePrompt):
    class Meta:
        text = "Enter the milestone due date in the format %s:" % DatePrompt.Meta.date_format
        label = "due date"


class ReportGenerationConfirmationPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Select the report number you wanna generate:"
        default = '1'

class ReportMilestonesPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Run report only on active milestones with the same identical name (created by gitlabcpc)?"
        default = 'yes'
        options = ['yes', 'no']
class ReportProjectsPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Run report on all projects or on a specific list?"
        default = 'yes'
        options = ['all', 'list']

class ReportMilestoneNamePrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Enter the milestone name:"

class LabelNamePrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Enter the label name:"

class LabelColorPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Enter the label color code:"

    def process_input(self):
        if len(self.input) < 7 or not self.input[0] == '#':
            print("You entered an invalid color format, color ignored")
            self.input = ''

class LabelCreationConfirmationPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Are you sure you wanna create this label across all your gitlab projects?"
        options = ['yes', 'no']
        default = 'no'
class LabelDeletionConfirmationPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Are you sure you want to delete this label across all your gitlab projects?"
        options = ['yes', 'no']
        default = 'no'
class IssueCloseConfirmationPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Are you sure you want to close all the issue which fall under this criteria?"
        options = ['yes', 'no']
        default = 'no'
class MilestoneNamePrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Enter the milestone name:"
    def process_input(self):
        if len(self.input) < 1:
            print("You did not specify a milestone name")
            self.input = ''

class IssuesExportProjectPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Enter project names in a comma separated list unless you wanna export every issue across all projects:"
        default = ''
    def process_input(self):
        if len(self.input) < 1:
            print("You didn't specify a project name, issues will be exported from all projects")
            self.input = ''
class IssuesExportLabelPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Wanna filter by label? enter the label name:"
        default = ''
    def process_input(self):
        if len(self.input) < 1:
            print("You didn't specify a label, issues will be exported regardless of labels")
            self.input = ''
class IssuesExportMilestonePrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Wanna filter by milestone? enter the milestone name:"
        default = ''
    def process_input(self):
        if len(self.input) < 1:
            print("You didn't specify a milestone, issues will be exported regardless of milestones")
            self.input = ''
class IssuesExportClosedPrompt(GitlabcpcBasePrompt):
    class Meta:
        text = "Include closed issues? [y/n]:"
        default = ''
    def process_input(self):
        if not self.input == 'y':
            print("will only export open issues")
            self.input = 'opened'
