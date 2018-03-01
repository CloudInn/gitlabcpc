from cement.core.controller import CementBaseController, expose
from prompts import *
from misc import *
import datetime
import sys
import csv

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

    @expose(help='Export issues into a csv file')
    def export(self):
        project_name = IssuesExportProjectPrompt().input
        label = IssuesExportLabelPrompt().input
        milestone = IssuesExportMilestonePrompt().input
        only_opened = IssuesExportClosedPrompt().input
        now = datetime.datetime.now()
        export_file = open('gitlab-issues-export-'+now.isoformat()[0:-7]+'.csv', 'w')
        fields = ['id', 'project', 'title', 'description', 'labels', 'milestone', 'time spent',
                'time estimated', 'author', 'assignee', 'due date', 'created',
                'closed', 'last modified', 'confidential', 'state', 'upvotes', 'downvotes']
        writer = csv.DictWriter(export_file, fieldnames=fields)
        writer.writeheader()

        if label == '' and milestone == '' and project_name == '':
            print("All issues from all projects will be exported")
        if not project_name == '':
            if not ',' in project_name:
                projects = self.app.gl.projects.list(search=project_name)
            else:
                projects = []
                for project in project_name.split(","):
                    projects = projects + self.app.gl.projects.list(search=project)
        else:
            projects = self.app.gl.projects.list(all=True)
        for project in projects:
            print('Exporting for project: %s' % project.name)
            if only_opened == 'opened':
                pages = project.issues.list(as_list=False, labels=[label], milestone=milestone, state='opened')
            else:
                pages = project.issues.list(as_list=False, labels=[label], milestone=milestone)
            i = 0
            while i < pages.total:
                issue = pages.next()
                milestone = issue.attributes['milestone']
                if milestone:
                    milestone_title = milestone['title']
                else:
                    milestone_title = ''
                assignee = issue.attributes['assignee']
                if assignee:
                    assignee = assignee['username']
                else:
                    assignee = ''
                writer.writerow({'id': issue.iid, 'project': project.name, 'title': issue.attributes['title'],
                    'description': issue.attributes['description'], 'labels': ';'.join(issue.attributes['labels']),
                    'milestone': milestone_title, 'time spent': issue.attributes['time_stats']['total_time_spent'],
                    'time estimated': issue.attributes['time_stats']['time_estimate'],
                    'author': issue.attributes['author']['username'], 'assignee': assignee,
                    'due date': issue.attributes['due_date'], 'created': issue.attributes['created_at'],
                    'closed': issue.attributes['closed_at'],
                    'last modified': issue.attributes['updated_at'], 'confidential': issue.attributes['confidential'],
                    'state': issue.state, 'upvotes': issue.attributes['upvotes'], 'downvotes': issue.attributes['upvotes'] })
                i = i + 1
            print('issues: %i' % i)
        print('Export results saved at: %s' % export_file.name)

