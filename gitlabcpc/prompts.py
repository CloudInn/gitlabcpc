"""Cement custom prompts

This module contains all the custom Cement prompts we'll use for all of our subcommands

"""

import sys
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
            start_date = datetime.strptime(self.input.lower() , '%Y-%m-%d')
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
        text = "Select the report number you wanna generate"
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
