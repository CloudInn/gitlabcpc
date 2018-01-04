from cement.utils import shell

def populate_gitlab_config():

    config = {}
    config['secret'] = shell.Prompt("Enter your Gitlab secret key:").input
    config['url'] = shell.Prompt("Enter the gitlab instance URL:").input
    config['name'] = shell.Prompt("Enter this gitlab instance's unique name:", default="default").input

    return config


def format_seconds(seconds):
    """Gitlab estimates, spent time is returned either in seconds or in a human readable format,
    in order to performa any operations on the time estimates the easiest way to do it is to use
    the seconds, perform any operations and then format the resut into a readable format"""

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def _get_working_hours(start_date, end_date, weekend_start="Sun"):
    """ Get the number of available work hours in a georgian calendar's date period.
    Assumptions made:
        - Weekends are two days long (Saturday & Sunday or Friday & Saturday)
        - every day has a maximum of 7 hours available
    """

    pass
