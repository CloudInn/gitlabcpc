from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from commands import *
from misc import *
import gitlab
import fnmatch


#gitlabcpc is a small utility command line tool which is used mainly to
#create milestones across all projects on a gitlab instance at once

__version__ = "1.0"


class MyApp(CementApp):
    class Meta:
        label = 'gitlabcpc'
        base_controller = 'base'
        extensions = ['tabulate']
        output_handler = 'tabulate'
        handlers = [base.BaseController, milestones.MilestonesController, reports.ReportsController, labels.LabelsController]


if __name__ == '__main__':
  with MyApp() as app:
    #Initiate a configuration file if it doesn't exist already.
    from os.path import expanduser
    home = expanduser("~")
    conf = open(home+"/.gitlabcpc.cnf", "a+")
    app.config.parse_file(home+"/.gitlabcpc.cnf")
    instances = fnmatch.filter(app.config.get_sections(), 'gl_*')

    if len(instances) < 1:
         config = populate_gitlab_config()
         app.config.add_section('gl_'+config['name'])
         app.config.set('gl_'+config['name'], 'url', config['url'])
         app.config.set('gl_'+config['name'], 'secret', config['secret'])
         app.config.write(conf)
    elif len(instances) > 1:
        #Select instance
        pass

    else:
        config = {'name': instances[0][3:],
                'url': app.config.get(instances[0], 'url'),
                'secret': app.config.get(instances[0], 'secret')
                }

    #Authenticate gitlab
    try:
        app.gl = gitlab.Gitlab(config['url'], config['secret'])

    except:
        print("Couldn't connect to the gitlab instance %t" % config['name'])

    app.run()
