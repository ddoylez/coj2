import argparse
import json
import random

MODES = [('historical', 'Wild West Legends'), ('deathmatch', 'Shootout'), ('teamdeathmatch', 'Posse'),
         ('wanted', 'Wanted'), ('teamwanted', 'Manhunt')]
DEFAULT_SERVER_NAME = 'Krampus in da House'
OUTPUT_FILE = 'DedicatedServerSettings.ini'
MAP_DEF_FILE = 'maps_def_mappings.json'
with open(MAP_DEF_FILE, 'r') as f:
    MAPS_DICT = json.load(f)


def get_parser(version='1.69'):
    parser = argparse.ArgumentParser(description='Generate a DedicatedServerSettings.ini for CoJ2')
    parser.add_argument('-i', '--internet-server', dest='internet_server', type=int, default=0, choices=[0, 1],
                        help='LAN = 0, Internet = 1, 0 by default')
    parser.add_argument('-ps', '--public-slots', dest='public_slots', type=int, default=12,
                        help='number of public slots (max players), 12 by default')
    parser.add_argument('-p2s', '--players-to-start', dest='players_to_start', type=int, default=1,
                        help='minimum number of players for the game to begin, 1 by default')
    parser.add_argument('-dp', '--points-limit-default', dest='points_limit_default', type=int, default=10,
                        help='target number of points for the game to end for teamwanted')
    parser.add_argument('-db', '--bounty-limit-default', dest='bounty_limit_default', type=int, default=500,
                        help='target of bounty for the game to end for applicable modes')
    parser.add_argument('-dt', '--time-limit-default', dest='time_limit_default', type=int, default=1200,
                        help='map time limit in seconds for applicable modes')
    parser.add_argument('-dmb', '--bounty-limit-deathmatch', dest='bounty_limit_deathmatch', type=int,
                        help='target of bounty for the game to end for deathmatch')
    parser.add_argument('-dmt', '--time-limit-deathmatch', dest='time_limit_deathmatch', type=int,
                        help='map time limit in seconds in for deathmatch')
    parser.add_argument('-tdmb', '--bounty-limit-teamdeathmatch', dest='bounty_limit_teamdeathmatch', type=int,
                        help='target of bounty for the game to end for teamdeathmatch')
    parser.add_argument('-tdmt', '--time-limit-teamdeathmatch', dest='time_limit_teamdeathmatch', type=int,
                        help='map time limit in seconds in for teamdeathmatch')
    parser.add_argument('-wb', '--bounty-limit-wanted', dest='bounty_limit_wanted', type=int,
                        help='target of bounty for the game to end for wanted')
    parser.add_argument('-wt', '--time-limit-wanted', dest='time_limit_wanted', type=int,
                        help='map time limit in seconds in for wanted')
    parser.add_argument('-twp', '--points-limit-teamwanted', dest='points_limit_teamwanted', type=int,
                        help='target number of points for the game to end in teamwanted')
    parser.add_argument('-twt', '--time-limit-teamwanted', dest='time_limit_teamwanted', type=int,
                        help='map time limit in seconds in for teamwanted')
    parser.add_argument('-ff', '--friendly-fire', dest='friendly_fire', type=int, default=1, choices=[0, 1],
                        help='Off = 0, On = 1, 1 by default')
    parser.add_argument('-name', '--server-name', dest='server_name', default=DEFAULT_SERVER_NAME,
                        help='server name visible on the server list')
    parser.add_argument('-pass', '--server-password', dest='server_password', default='',
                        help='password for starting the server')
    parser.add_argument('-port', '--server-port', dest='server_port', type=int, default=27632,
                        help='port the server is running on, 27632 by default')
    parser.add_argument('-m', '--mode', dest='modes', action='append', choices=[mode[0] for mode in MODES],
                        help='can specify multiple times, deathmatch by default')
    parser.add_argument('-l', '--map-limit', dest='map_limit', type=int, default=None,
                        help='limit how many "Map" entries are made, unlimited by default')
    parser.add_argument('-c', '--custom-maps', dest='custom_maps', default=False,
                        action=argparse.BooleanOptionalAction, help='adds custom maps into selection pool')
    parser.add_argument('-o', '--output-file', dest='output_file', default=OUTPUT_FILE,
                        help='file to write settings to')
    parser.add_argument('-s', '--seed', dest='seed', default=None,
                        help='seed for map shuffle')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v{}'.format(version))
    return parser


def parse_args(parser):
    return parser.parse_args()


def ss_setting(name, s1, s2):
    return f'{name}(\"{s1}\", \"{s2}\")\n'


def si_setting(name, s, i):
    return f'{name}(\"{s}\", {i})\n'


def s_setting(name, s):
    return f'{name}(\"{s}\")\n'


def i_setting(name, i):
    return f'{name}({i})\n'


def generate_definitions():
    settings = ['!Map(s, s)\n', '!InternetServer(i)\n', '!PublicSlots(i)\n', '!PlayersToStart(i)\n',
                '!PointsLimitDefault(i)\n', '!BountyLimitDefault(i)\n', '!TimeLimitDefault(i)\n',
                '!PointsLimit(s, i)\n', '!BountyLimit(s, i)\n', '!TimeLimit(s, i)\n', '!FriendlyFire(i)\n',
                '!ServerName(s)\n', '!ServerPassword(s)\n', '!ServerPort(i)\n', '\n']
    return settings


def generate_server(args):
    settings = [s_setting('ServerName', args.server_name), s_setting('ServerPassword', args.server_password),
                i_setting('ServerPort', args.server_port), '\n', i_setting('InternetServer', args.internet_server),
                i_setting('FriendlyFire', args.friendly_fire), i_setting('PublicSlots', args.public_slots),
                i_setting('PlayersToStart', args.players_to_start), '\n',
                i_setting('PointsLimitDefault', args.points_limit_default),
                i_setting('BountyLimitDefault', args.bounty_limit_default),
                i_setting('TimeLimitDefault', args.time_limit_default), '\n']
    return settings


def get_map_set(set_tag):
    map_set = []
    for level in MAPS_DICT:
        if (set_tag == MAPS_DICT[level]['map_set']) and (eval(MAPS_DICT[level]['in_rotation'])):
            map_set.append(level)
    return map_set


def get_map_pool(use_custom_maps):
    map_pool = get_map_set('base')
    if use_custom_maps:
        # map_pool.extend(get_map_set('dlc'))
        map_pool.extend(get_map_set('custom'))
        map_pool.extend(get_map_set('heaven'))
    return map_pool


def get_mode_pool(modes):
    mode_pool = []
    if modes:
        for mode in modes:
            if mode not in mode_pool:
                mode_pool.append(mode)
    else:
        mode_pool.append('deathmatch')
    return mode_pool


def generate_map_tuples(map_pool, mode_pool):
    map_tuples = []
    for mode in mode_pool:
        for level in map_pool:
            map_modes = MAPS_DICT[level]['modes']
            if mode in map_modes:
                map_tuples.append((level, mode))
    return map_tuples


def generate_mode(args):
    settings = []
    mode_args = {'teamwanted': [args.points_limit_teamwanted, args.time_limit_teamwanted],
                 'wanted': [args.bounty_limit_wanted, args.time_limit_wanted],
                 'teamdeathmatch': [args.bounty_limit_teamdeathmatch, args.time_limit_teamdeathmatch],
                 'deathmatch': [args.bounty_limit_deathmatch, args.time_limit_deathmatch]}
    for mode in mode_args:
        if mode_args[mode][0]:
            if mode == 'teamwanted':
                limit_name = 'PointsLimit'
            else:
                limit_name = 'BountyLimit'
            settings.append(si_setting(limit_name, mode, mode_args[mode][0]))
        if mode_args[mode][1]:
            settings.append(si_setting('TimeLimit', mode, mode_args[mode][1]))
    if len(settings) > 0:
        settings.append('\n')
    return settings


def generate_levels(map_tuples, limit, seed):
    settings = []
    random.seed(seed)
    random.shuffle(map_tuples)
    for level in map_tuples[:limit]:
        settings.append(ss_setting('Map', level[0], level[1]))
    return settings


def generate_file(args):
    settings = []
    settings.extend(generate_definitions())
    settings.extend(generate_server(args))
    map_pool = get_map_pool(args.custom_maps)
    mode_pool = get_mode_pool(args.modes)
    map_tuples = generate_map_tuples(map_pool, mode_pool)
    settings.extend(generate_mode(args))
    settings.extend(generate_levels(map_tuples, args.map_limit, args.seed))
    return settings


def print_settings(settings):
    for line in settings:
        print(line, end='')


def write_settings(settings, file_name):
    with open(file_name, 'w') as file:
        for line in settings:
            file.write(line)


def main():
    print(MAPS_DICT)
    args = parse_args(get_parser())
    settings = generate_file(args)
    print_settings(settings)
    write_settings(settings, args.output_file)


if __name__ == "__main__":
    main()
