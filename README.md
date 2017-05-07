# Slack-Eve-Killmail Docker

## Requirements
* Slack
* Python 2

## Install Instructions
* In Slack, go to /services/new, select Incoming WebHooks. 
	* Fill in channel/name
	* Copy URL to SLACK\_KILLMAIL\_URL environment variable
* In SLACK\_KILLMAIL\_OWNER configure which alliances to track
	* Format is key:value
	* Comma separated corporation or alliance to track
	* Key is allianceID or corporationID
	* Value is the ID
		* Go to [zkillboard](https://zkillboard.com/)
		* Search your corp/alliance
		* ID is in URL behind /corporation/ or /alliance/
* If you haven't already, bind corporation API key to zkillboard to get all kills listed
* Build Dockerfile and run

## Configurable environment variables
* SLACK\_KILLMAIL\_OWNER = "" # Format of: corporationID:id,allianceID:id
* SLACK\_KILLMAIL\_CHECK\_TIME = '86400' # Check for the last day
* SLACK\_KILLMAIL\_SLEEP\_TIME = '1200' # Delay between checks
* SLACK\_KILLMAIL\_URL = 'https://hooks.slack.com/services/' # Slack integration code
* SLACK\_KILLMAIL\_PARTICIPATING = 'False' # Shows the top 10 participating pilots on the kills that are part of your corporation or alliance
* SLACK\_KILLMAIL\_EXTENDED\_NAME = 'False' # If True, shows (corporationName) on both victim and attacker

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
