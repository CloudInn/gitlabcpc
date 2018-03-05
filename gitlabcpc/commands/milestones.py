import collections
from cement.core.controller import CementBaseController, expose
from cement.utils import shell
from prompts import (MilestonesCreationDescriptionPrompt,
                     MilestonesCreationStartDatePrompt,
                     MilestonesCreationDueDatePrompt,
                     MilestonesCreationConfirmationPrompt)


class MilestonesController(CementBaseController):
    class Meta:
        label = 'milestones'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Milestones management subcommand."
        arguments = [
            (['-sd', '--start-date'],
             dict(action='store', help='The start date of the milestone')),
            (['-dd', '--due-date'],
             dict(action='store', help='the end date of the milestone')),
            (['--name'],
             dict(action='store', help='the milestone name')),
            (['-desc', '--description'],
             dict(action='store', help='the milestone description')),
            (['-id', '--milestone-id'],
             dict(action='store', help='the ID for the milestone being edited'
                  )),
            (['-ed', '--end-date'],
             dict(action='store', help='the end date of the milestone')),
        ]

    @expose(help='Milestones management', aliases=['mlst'])
    def default(self):
        self.app.log.info("start date: %s" % self.app.pargs.start_date)

    @expose(help='Create new milestone')
    def create(self):
        milestone = collections.OrderedDict()
        milestone['title'] = shell.Prompt("Enter the milestone title:").input
        milestone['description'] = MilestonesCreationDescriptionPrompt().input
        milestone['start_date'] = MilestonesCreationStartDatePrompt().input
        milestone['due_date'] = MilestonesCreationDueDatePrompt().input
        self.app.render([milestone.values()], headers=milestone.keys())

        proceed = MilestonesCreationConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.list(per_page=100):
                print("Creating milestone for project %s...." % project.name)
                project.milestones.create(milestone)
        else:
            print('Milestone creation canceled')

    @expose(help='list active milestones')
    def list(self):
        projects = self.app.gl.projects.list(per_page=100)
        i = 0
        for project in projects:
            for milestone in project.milestones.list(state='active'):
                i += 1
                print(milestone.title)
        print("Total active milestones across all projects: %d" % i)

    def edit(self):
        self.app.log.info('edit a milestone')

    def activate(self):
        self.app.log.info('activate a milestone')

    def close(self):
        self.app.log.info('Close a milestone')
