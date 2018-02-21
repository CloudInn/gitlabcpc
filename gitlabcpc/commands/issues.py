from cement.core.controller import CementBaseController, expose
from prompts import *
from misc import *
import sys

class IssuesController(CementBaseController):
    class Meta:
        label = 'issues'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "issues management subcommand."

    @expose(help='Gitlab issues management', aliases=['isl'])
    def default(self):
        print("Use one of the close, open subcommands")

    @expose(help='Close issues based on a label & a milestone')
    def close(self):
        label_name = LabelNamePrompt().input
        if label_name == '':
            print("A label must be provided")
            sys.exit(1)
        milestone = MilestoneNamePrompt().input
        proceed = IssueCloseConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.all(per_page=100):
                closed = 0
                for issue in project.issues.list(milestone=milestone, labels=[label_name], state='opened', per_page=100):
                    issue.state_event = 'close'
                    issue.save()
                    closed += 1
                print("Closed %i for the project %s" % (closed, project.name))
