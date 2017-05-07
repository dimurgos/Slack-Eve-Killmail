from os import getenv

def create_owner(config_owner_string):
    tmp_config_owner = []
    for owner_string in config_owner_string.split(','):
        owner = owner_string.split(':')
        obj = {}
        obj[owner[0]] = int(owner[1])
        tmp_config_owner.append(obj)
    return tmp_config_owner

config_header = 'Slack-Eve-Killboard/1.1a https://github.com/dimurgos/Slack-Eve-Killmail' # header
config_owner = create_owner(getenv('SLACK_KILLMAIL_OWNER', '')) # Format of: corporationID:id,allianceID:id (can be multiple)
config_check = getenv('SLACK_KILLMAIL_CHECK_TIME', '86400') # Check for the last day
config_sleep_time = int(getenv('SLACK_KILLMAIL_SLEEP_TIME', '1200')) # Delay between checks
config_slack_url = getenv('SLACK_KILLMAIL_URL', 'https://hooks.slack.com/services/') # Slack integration code
config_run_as_daemon = False
config_show_participating = getenv('SLACK_KILLMAIL_PARTICIPATING', 'False') == 'True' # Shows the top 10 participating pilots on the kills that are part of your corporation or alliance
config_extended_name = getenv('SLACK_KILLMAIL_EXTENDED_NAME', 'False') == 'True' # If True, shows (corporationName) on both victim and attacker

### Locales
#config_locale = 'English_United States' # Windows locale
config_locale = 'en_US' # Generic linux/mac locale
#config_locale = 'en_US.UTF-8' # Ubuntu linux locale
#config_locale = '' # Use default locale
### Locales
