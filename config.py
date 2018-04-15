config_header = 'Slack-Eve-Killboard/1.1a https://github.com/dimurgos/Slack-Eve-Killmail' # header
config_owner = [{'': 0}] # Format of: 'corporationID': <id> or 'allianceID': <id> (can be multiple)
config_check = '86400' # Check for the last day
config_sleep_time = 1200 # Delay between checks
config_slack_url = 'https://hooks.slack.com/services/' # Slack integration code
config_run_as_daemon = False
config_show_participating = False # Shows the top 10 participating pilots on the kills that are part of your corporation or alliance
config_extended_name = False # If True, shows (corporationName) on both victim and attacker
config_discord = False # If True, properly posts for discord

config_minimum_value = 0 # Minimum kill value

### Locales
#config_locale = 'English_United States' # Windows locale
config_locale = 'en_US' # Generic linux/mac locale
#config_locale = 'en_US.UTF-8' # Ubuntu linux locale
#config_locale = '' # Use default locale
### Locales
