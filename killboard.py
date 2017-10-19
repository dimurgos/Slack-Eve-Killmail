#!/usr/bin/env python
import urllib2
import urllib
import json
import sys
import exceptions
import locale
import config
import systems
import ships
import alliances
import characters
import corporations
from datetime import datetime
import time
import os
import signal

def run_killboard(config_type, config_id):
    kills = 'https://zkillboard.com/api/{0}/{1}/pastSeconds/{2}/orderDirection/asc/'.format(config_type, config_id, config.config_check)

    if config_type == 'corporationID':
       config_type = 'corporation_id'
    if config_type == 'allianceID':
       config_type = 'alliance_id'
    if config_type == 'characterID':
       config_type = 'character_id'
    
    locale.setlocale(locale.LC_ALL, config.config_locale)

    request = urllib2.Request(kills)
    request.add_header('User-Agent', config.config_header)
    opener = urllib2.build_opener()
    data = opener.open(request)
    root = json.load(data)

    handled_kills = []
    f = open('handled_kills.dat', 'r+')
    for line in f:
        handled_kills.append(line.rstrip('\n'))

    for record in root:
        try:
            killmail_id = record['killmail_id']
            if str(killmail_id) in handled_kills:
                continue
            
            killers = []
            highestDealer = None
            killer = {}
            attackerCount = 0
            highestDmg = -1
            for attacker in record['attackers']:
                if attacker['final_blow'] == 1:
                    killer = attacker
                if 'character_id' not in attacker and attacker['faction_id'] != 0:
                    continue
                else:
                    attackerCount += 1
                if attacker['character_id'] != 0 and attacker['damage_done'] > highestDmg:
                    highestDmg = attacker['damage_done']
                    highestDealer = attacker
                if config.config_show_participating and attacker[config_type] == config_id:
                    character_name = characters.get_character_by_id(attacker['character_id'])
                    corporation_name = corporations.get_corporation_by_id(attacker['corporation_id'])
                    killers.append({'character_name': character_name, 'character_id': attacker['character_id'], 'corporation_name': corporation_name, 'corporation_id': attacker['corporation_id'], 'damage_done': attacker['damage_done']})

            victim = record['victim']

            attachment = {}
            damageTaken = {}
            kill = {}

            if 'character_id' not in killer:
                killerName = killer['ship_type_id']
            else:
                killerName = characters.get_character_by_id(killer['character_id'])
            if 'character_id' not in victim:
                victimName = victim['ship_type_id']
            else:
                victimName = characters.get_character_by_id(victim['character_id'])
            
            if victim[config_type] == config_id:
                if config.config_extended_name: 
                    if 'alliance_id' not in killer:
                        allianceName = ''
                    else:
                        allianceName = ' ({0})'.format(alliances.get_alliance_by_id(killer['alliance_id']))
                    kill['fallback'] = '{0} ({1}) got killed by {2} ({3}){4}'.format(victimName, corporations.get_corporation_by_id(victim['corporation_id']), killerName, corporations.get_corporation_by_id(killer['corporation_id']), allianceName)
                else:
                    kill['fallback'] = '{0} got killed by {1} ({2})'.format(victimName, killerName, corporations.get_corporation_by_id(killer['corporation_id']))
                kill['color'] = 'danger'
                damageTaken['title'] = "Damage taken"
            else:
                if config.config_extended_name: 
                    if 'alliance_id' not in victim:
                        allianceName = ''
                    else:
                        allianceName = ' ({0})'.format(alliances.get_alliance_by_id(victim['alliance_id']))
                    kill['fallback'] = '{0} ({1}) killed {2} ({3}){4}'.format(killerName, corporations.get_corporation_by_id(killer['corporation_id']), victimName, corporations.get_corporation_by_id(victim['corporation_id']), allianceName)
                else:
                    kill['fallback'] = '{0} killed {1} ({2})'.format(killerName, victimName, corporations.get_corporation_by_id(victim['corporation_id']))
                kill['color'] = 'good'
                damageTaken['title'] = "Damage dealt"
                
            kill['title'] = kill['fallback']
            kill['title_link'] = 'https://zkillboard.com/kill/{0}/'.format(killmail_id)
            kill['thumb_url'] = 'https://imageserver.eveonline.com/Render/{0}_64.png'.format(victim['ship_type_id'])
            
            damageTaken['value'] = locale.format('%d', victim['damage_taken'], grouping=True)
            damageTaken['short'] = "true"
            
            value = {'title': 'Value', 'value': locale.format('%d', record['zkb']['totalValue'], grouping=True) + ' ISK', 'short': False}
            totalAttackers = {'title': 'Pilots involved', 'value': str(attackerCount), 'short': 'true'}

            mostDmg = {}
            if highestDealer and highestDealer['character_id'] != 0:
                mostDmg['title'] = 'Most Damage'
                mostDmg['value'] = '<https://zkillboard.com/character/{0}|{1}> ({2})'.format(highestDealer['character_id'], characters.get_character_by_id(highestDealer['character_id']), locale.format('%d', highestDmg, grouping=True))
                mostDmg['short'] = "true"

            solarSystemName,regionID,regionName,constellationName,security = systems.get_system_by_id(record['solar_system_id'])
            system = {'title': 'System', 'value': '<https://zkillboard.com/system/{systemID}|{systemName}> ({security:.1g}) / <https://zkillboard.com/region/{regionID}|{regionName}> / {constellationName}'.format(
                systemID = record['solar_system_id'], 
                systemName = solarSystemName, 
                security = security,
                regionName = regionName,
                regionID = regionID,
                constellationName = constellationName
            ), 'short': False}
            ship = {'title': 'Ship', 'value': '{0}'.format(ships.get_ship_by_id(victim['ship_type_id'])), 'short': 'true'}
            
            if config.config_show_participating:
                row_damage = {'fallback': kill['fallback'], 'color': kill['color'], 'title': kill['title'], 'title_link': kill['title_link'], 'fields': [damageTaken, totalAttackers], 'thumb_url': 'https://imageserver.eveonline.com/Corporation/{0}_64.png'.format(victim['corporation_id'])}
                row_ship = {'color': kill['color'], 'fields': [mostDmg, ship], 'thumb_url': kill['thumb_url']}
                row_value = {'color': kill['color'], 'fields': [value]}
                row_system = {'color': kill['color'], 'fields': [system]}
                attachment['attachments'] = [row_damage, row_ship, row_value, row_system]
                i = 0
                for attacker in killers:
                    attacker_name = {'title': 'Attacker', 'value': '<https://zkillboard.com/character/{0}|{1}> ({2})'.format(attacker['character_id'], characters.get_character_by_id(attacker['character_id']), corporations.get_corporation_by_id(attacker['corporation_id'])), 'short': 'true'}
                    attacker_damage = {'title': 'Damage Done', 'value': locale.format('%d', attacker['damage_done'], grouping=True), 'short': 'true'}
                    attachment['attachments'].append({'color': kill['color'], 'fields': [attacker_name, attacker_damage], 'thumb_url': 'https://imageserver.eveonline.com/Corporation/{0}_64.png'.format(attacker['corporation_id'])})
                    i += 1
                    if i == 10:
                        break
            else:
                kill['fields'] = [damageTaken, totalAttackers, mostDmg, ship, value, system]
                attachment['attachments'] = [kill]
            
            data = json.dumps(attachment)
            
            if not config.config_discord:
                data = urllib.urlencode({'payload': data})
                request_slack = urllib2.Request(config.config_slack_url, data)
            else:
                request_slack = urllib2.Request(config.config_slack_url, data, {'User-Agent': config.config_header})
            urllib2.urlopen(request_slack)

            time.sleep(2)
            f.write('{0}\n'.format(killmail_id))
        except urllib2.HTTPError as e:
            print "HTTPError in processing record: " + str(e.reason)
        except exceptions.KeyError as e:
            print "KeyError in processing record: " + str(e)
        except exceptions.NameError as e:
            print "NameError in processing record: " + str(e)
        except Exception:
            print "Generic Exception in processing record: " + str(sys.exc_info()[0]) + " (" + str(sys.exc_info()[1]) + ")"
        
    f.close()
    
def make_pid():
    try:
        os.stat('/var/run')
    except:
        os.mkdir('/var/run')
    f = open('/var/run/kbbot.pid', 'w+')
    f.truncate()
    f.write(str(os.getpid()))
    f.write("\n");
    f.close()

def signal_handler(signal, frame):
    os.remove('/var/run/kbbot.pid')
    exit()

if config.config_run_as_daemon:
    make_pid()
    signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        for group in config.config_owner:
            for key,val in group.items():
                run_killboard(key, val)
            time.sleep(60)
        time.sleep(config.config_sleep_time)
    except urllib2.HTTPError as e:
        print "HTTPError in processing killboard data: " + str(e.reason)
        time.sleep(60)
    except Exception:
        print "Exception in processing killboard data: " + str(sys.exc_info()[0]) + " (" + str(sys.exc_info()[1]) + ")"
        time.sleep(60)
