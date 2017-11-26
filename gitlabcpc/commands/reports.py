import collections
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.utils import shell
from prompts import *
from misc import *
import reports
import copy

class ReportsController(CementBaseController):
    class Meta:
        label = 'reports'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "reports generation subcommand."
        arguments = [ ( [ '-ac', '--active'], dict(action='store', help='Generate the report only on the active sprints (Default: yes)')),
                (['-all', '--all-projects'], dict(action='store', help='Generate the report on all the projects (Default: yes')),
                (['-ml', '--milestone-name'], dict(action='store', help='Milestone name (if multiple projects share the same milestone name the report will be generated across all projects)'))
                ]

    @expose(help='Gitlab basic reporting', aliases=['rpt'])
    def default(self):
        self.app.log.info("start date: %s" % self.app.pargs.start_date)
    @expose(help='Generate report')
    def generate(self):
        i = 0
        options = {}
        for report in reports.__all__:
            if report == 'base':
                continue
            i += 1
            rp = __import__("reports." + report, fromlist=[''])
            print(str(i)+") "+report+" - "+str(rp.__doc__))
            options[i] = copy.deepcopy(report)
        gen = int(ReportGenerationConfirmationPrompt().input)

        report = __import__("reports."+ options[gen], fromlist=[''])
        report = report.Report(self.app.gl, self.app.pargs)
        report.generate()
