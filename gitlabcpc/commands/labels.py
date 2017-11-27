import collections
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.utils import shell
from prompts import *
from misc import *
import reports
import copy

class LabelsController(CementBaseController):
    class Meta:
        label = 'labels'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "labels management subcommand."

    @expose(help='Gitlab labels management', aliases=['lbl'])
    def default(self):
        print("Use one of the create, edit, delete subcommands")

    @expose(help='Create a label across all projects')
    def create(self):
        label = {}
        label['name'] = LabelNamePrompt().input
        if label['name'] == '':
            print("You can't create a label with an empty name")
            sys.exit(1)
        label['color'] = LabelColorPrompt().input

        proceed = LabelCreationConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.all(per_page=100):
                print("Creating label for project %s" % project.name)
                project.labels.create(label)
