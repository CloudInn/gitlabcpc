from cement.core.controller import CementBaseController, expose
from prompts import (BranchNamePrompt, BranchCreationConfirmationPrompt,
                     BranchDeletionConfirmationPrompt,
                     BranchProtectConfirmationPrompt,
                     BranchUnprotectConfirmationPrompt,
                     BranchSetDefaultConfirmationPrompt,
                     RefBranchNamePrompt)
from gitlab.exceptions import (GitlabCreateError, GitlabAuthenticationError,
                               GitlabUpdateError, GitlabDeleteError,
                               GitlabGetError)
import sys


class BranchesController(CementBaseController):
    class Meta:
        label = 'branches'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "branches management subcommand."

    def print_info(self, msg):
        txt = '\x1b[6;30;44m%s\x1b[0m %s' % ('INFO!', msg)
        print(txt)

    def print_warning(self, msg):
        txt = '\x1b[6;30;43m%s\x1b[0m %s' % ('WARNING!', msg)
        print(txt)

    def print_error(self, msg):
        txt = '\x1b[6;30;41m%s\x1b[0m %s' % ('ERROR!', msg)
        print(txt)

    @expose(help='Gitlab branches management')
    def default(self):
        print("Use one of the create, delete, protect, unprotect and "
              "set_default subcommands")

    @expose(help='Delete a branch across all projects')
    def delete(self):
        branch_name = BranchNamePrompt().input
        if branch_name == '':
            print("A branch must have a name")
            sys.exit(1)
        proceed = BranchDeletionConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.all(per_page=100):
                try:
                    branch = project.branches.get(branch_name)
                except (GitlabGetError, GitlabAuthenticationError):
                    self.print_warning("Branch doesn't exist for the project "
                                       "%s" % project.name)
                    continue
                try:
                    if branch.delete():
                        self.print_info("Deleted branch for project %s" %
                                        project.name)
                    else:
                        self.print_error("Failed to delete the branch, check "
                                         "your gitlab permissions")
                except (GitlabAuthenticationError, GitlabDeleteError):
                        self.print_error("Failed to delete the branch, check "
                                         "your gitlab permissions")

    @expose(help='Protect a branch across all projects')
    def protect(self):
        branch_name = BranchNamePrompt().input
        if branch_name == '':
            print("A branch must have a name")
            sys.exit(1)
        proceed = BranchProtectConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.all(per_page=100):
                try:
                    branch = project.branches.get(branch_name)
                except (GitlabGetError, GitlabAuthenticationError):
                    self.print_warning("Branch doesn't exist for the project "
                                       "%s" % project.name)
                    continue
                branch.protect()
                if branch.protected:
                    self.print_info("Protected branch for project %s"
                                    % project.name)
                else:
                    self.print_error("Failed to protect the branch, check "
                                     "your gitlab permissions")

    @expose(help='Unprotect a branch across all projects')
    def unprotect(self):
        branch_name = BranchNamePrompt().input
        if branch_name == '':
            print("A branch must have a name")
            sys.exit(1)
        proceed = BranchUnprotectConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.all(per_page=100):
                try:
                    branch = project.branches.get(branch_name)
                except (GitlabGetError, GitlabAuthenticationError):
                    self.print_warning("Branch doesn't exist for the project "
                                       "%s" % project.name)
                    continue
                branch.unprotect()
                if not branch.protected:
                    self.print_info("Unprotected branch for project %s" %
                                    project.name)
                else:
                    self.print_error("Failed to set default branch, check "
                                     "your gitlab permissions for project "
                                     "%s" % project.name)

    @expose(help='Set default branch across all projects')
    def set_default(self):
        branch_name = BranchNamePrompt().input
        if branch_name == '':
            print("A branch must have a name")
            sys.exit(1)
        proceed = BranchSetDefaultConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.all(per_page=100):
                try:
                    project.branches.get(branch_name)
                except (GitlabGetError, GitlabAuthenticationError):
                    self.print_warning("Branch doesn't exist for the project "
                                       "%s" % project.name)
                    continue
                project.default_branch = branch_name
                try:
                    project.save()
                    self.print_info("Default branch set for project %s" %
                                    project.name)
                except (GitlabUpdateError, GitlabAuthenticationError):
                    self.print_error("Failed to set default branch, check "
                                     "your gitlab permissions for project %s"
                                     % project.name)

    @expose(help='Create branch across all projects')
    def create(self):
        branch_name = BranchNamePrompt().input
        if branch_name == '':
            print("New branch must have a name")
            sys.exit(1)
        ref_branch_name = RefBranchNamePrompt().input
        if ref_branch_name == '':
            print("You must enter reference branch name")
            sys.exit(1)
        proceed = BranchCreationConfirmationPrompt().input
        if proceed == 'yes':
            for project in self.app.gl.projects.all(per_page=100):
                try:
                    project.branches.create({'branch': branch_name,
                                             'ref': ref_branch_name})
                    self.print_info("Created branch for project %s" %
                                    project.name)
                except (GitlabCreateError, GitlabAuthenticationError):
                    self.print_error("Failed to create branch, check your "
                                     "gitlab permissions for project %s" %
                                     project.name)
