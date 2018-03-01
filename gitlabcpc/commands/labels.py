from cement.core.controller import CementBaseController, expose
from prompts import (LabelNamePrompt,
                     LabelColorPrompt,
                     LabelCreationConfirmationPrompt,
                     LabelDeletionConfirmationPrompt)
from gitlab.exceptions import (GitlabAuthenticationError,
                               GitlabGetError)
import sys


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
                try:
                    project.labels.get(label['name'])
                    print("Label already exists for the project %s" %
                          project.name)
                    continue
                except (GitlabGetError, GitlabAuthenticationError):
                    if project.labels.create(label):
                        print("Created label for project %s" % project.name)
                    else:
                        print("Failed to create the label, check your "
                              "gitlab permissions")

    @expose(help='Delete a label across all projects')
    def delete(self):
        label = {}
        label_name = LabelNamePrompt().input
        if label_name == '':
            print("A label must have a name")
            sys.exit(1)
        proceed = LabelDeletionConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.all(per_page=100):
                try:
                    label = project.labels.get(label_name)
                except (GitlabGetError, GitlabAuthenticationError):
                    print("Label doesn't exist for the project %s" %
                          project.name)
                    continue
                if label.delete():
                    print("Deleted label for project %s" % project.name)
                else:
                    print("Failed to delete the label, check your "
                          "gitlab permissions")
