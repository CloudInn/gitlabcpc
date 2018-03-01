from cement.core.controller import CementBaseController, expose


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "cross projects gitlab command line tool."

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()
