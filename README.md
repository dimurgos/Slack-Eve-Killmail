# Slack-Eve-Killmail

## Requirements
* Slack
* Python 2

## Install Instructions
* In Slack, go to /services/new, select Incoming WebHooks. 
	* Fill in channel/name
	* Copy URL in config.py in the config\_slack\_url
* In config.py configure which alliances to track
	* Format is dictionary in array
	* Each dictionary in the array is a separate corporation or alliance to track
	* Key is allianceID or corporationID
	* Value is the ID
		* Go to [zkillboard](https://zkillboard.com/)
		* Search your corp/alliance
		* ID is in URL behind /corporation/ or /alliance/
* If you haven't already, bind corporation API key to zkillboard to get all kills listed
* If on ubuntu, copy or symlink scripts/ubuntu.init to /etc/init.d/kbbot and run `update-rc.d kbbot defaults`

## Configurable fields
* config\_header = 'Slack-Eve-Killboard/1.0a https://github.com/dimurgos/Slack-Eve-Killmail' # header
* config\_owner = [{'': 0}] # Format of: 'corporationID': <id> or 'allianceID': <id> (can be multiple)
* config\_check = '86400' # Check for the last day (maximal retrieval amount)
* config\_sleep\_time = 1200 # Delay between checks (20 minutes default)
* config\_slack\_url = 'https://hooks.slack.com/services/' # Slack integration code
* config\_locale = 'en\_US' # The locale to post ISK values in
* config\_run\_as\_daemon = False # Tries to run as daemon instead of keeping the application alive
* config\_show\_participating = False # True shows the top 10 participating pilots on the kills that are part of your corporation or alliance (default to False), see example below.
* config\_extended\_name = False # If True, shows (corporationName) on both victim and attacker
* config\_discord = False # If True, properly posts for discord

## Result
* Every 20 minutes the list of kills over the last day will be posted in the configured Slack channel
* Posts if it is a loss or a kill (green for kill, red for loss)
* Includes damage dealt, pilots involved, ship, value, system and most damage done

## Example config\_show\_participating = False
![example](docs/killmails.png?raw=true)

## Example config\_show\_participating = True
![example](docs/multi\_kill\_example.png?raw=true)

## Example config\_extended\_name = True
![example](docs/extended\_names.png?raw=true)

## Solutions for possible issues
* 'locale.Error'
	* If this happens, check your locales if the current configured value is supported. Some possible values have been added as suggestions.
* 'IOError'
	* Usually relates to missing database file 'handled_kills.dat', create if not available.
* Exception in processing record: '(corp id)' 
	* Check if config\_owner is configured like follows: 
		* config\_owner = [{'corporationID': (corp id)}]
