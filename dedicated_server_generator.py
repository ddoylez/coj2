import argparse
import random

MAPS = [('Adobes', 'Taos Pueblo'), ('Civil', 'Burnside\'s Bridge'), ('Coffeyville', 'Coffeyville'),
        ('Frisco', 'Frisco'), ('Magnificent', 'Magnificent'), ('PrisonBreak2', 'Nogales'),
        ('StrinkingSprings2', 'Stinking Springs'), ('Tombstone', 'Tombstone')]
CUSTOM_MAPS = [('somerton', 'Somerton'), ('pancho', 'Pancho'), ('new_bouquet', 'New Bouquet'),
               ('calico_ghost_town', 'Bandits Secret Hideout'), ('calico_ghost_town2', 'Calico Ghost Town'),
               ('little_canyon', 'Little_Canyon'), ('green_hell', 'Green_Hell'), ('enclosure', 'Enclosure'),
               ('cursed_land', 'Cursed_land'), ('last_bullet_rebirth', 'N/A')]
MODES = [('historical', 'Wild West Legends'), ('deathmatch', 'Shootout'), ('teamdeathmatch', 'Posse'),
         ('wanted', 'Wanted'), ('teamwanted', 'Manhunt')]
DEFAULT_SERVER_NAME = 'Krampus in da House'
OUTPUT_FILE = 'DedicatedServerSettings.ini'


def strip_arr(arr, pos):
    new_arr = []
    for i in arr:
        new_arr.append(i[pos])
    return new_arr


def get_parser(version='0.69'):
    parser = argparse.ArgumentParser(description='Generate a DedicatedServerSettings.ini for CoJ2')
    parser.add_argument('-i', '--internet-server', dest='internet_server', type=int, default=0, choices=[0, 1],
                        help='LAN = 0, Internet = 1, 0 by default')
    parser.add_argument('-ps', '--public-slots', dest='public_slots', type=int, default=12,
                        help='number of public slots (max players), 12 by default')
    parser.add_argument('-p2s', '--players-to-start', dest='players_to_start', type=int, default=1,
                        help='minimum number of players for the game to begin, 1 by default')
    parser.add_argument('--points-limit-default', dest='points_limit_default', type=int, default=10,
                        help='target number of points for the game to end for teamwanted')
    parser.add_argument('--bounty-limit-default', dest='bounty_limit_default', type=int, default=1000,
                        help='target of bounty for the game to end for applicable modes')
    parser.add_argument('--time-limit-default', dest='time_limit_default', type=int, default=1200,
                        help='map time limit in seconds for applicable modes')
    parser.add_argument('-p', '--points-limit', dest='points_limit', type=int,
                        help='target number of points for the game to end in teamwanted')
    parser.add_argument('-b', '--bounty-limit', dest='bounty_limit', type=int,
                        help='target of bounty for the game to end for applicable modes')
    parser.add_argument('-t', '--time-limit', dest='time_limit', type=int,
                        help='map time limit in seconds in for applicable modes')
    parser.add_argument('-ff', '--friendly-fire', dest='friendly_fire', type=int, default=1, choices=[0, 1],
                        help='Off = 0, On = 1, 1 by default')
    parser.add_argument('-name', '--server-name', dest='server_name', default=DEFAULT_SERVER_NAME,
                        help='server name visible on the server list')
    parser.add_argument('-pass', '--server-password', dest='server_password', default='',
                        help='password for starting the server')
    parser.add_argument('-port', '--server-port', dest='server_port', type=int, default=27632,
                        help='port the server is running on, 27632 by default')
    parser.add_argument('-m', '--mode', dest='modes', action='append', default=['deathmatch'],
                        choices=[mode[0] for mode in MODES], help='can specify multiple times, deathmatch by default')
    parser.add_argument('-l', '--map-limit', dest='map_limit', type=int, default=None,
                        help='limit how many "Map" entries are made, unlimited by default')
    parser.add_argument('-c', '--custom-maps', dest='custom_maps', default=False,
                        action=argparse.BooleanOptionalAction, help='adds custom maps into selection pool')
    parser.add_argument('-o', '--output-file', dest='output_file', default=OUTPUT_FILE,
                        help='file to write settings to')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v{}'.format(version))
    return parser


def parse_args(parser):
    return parser.parse_args()


def ss_setting(name, s1, s2):
    setting = f'{name}(\"{s1}\", \"{s2}\")\n'
    return setting


def si_setting(name, s, i):
    setting = f'{name}(\"{s}\", {i})\n'
    return setting


def s_setting(name, s):
    setting = f'{name}(\"{s}\")\n'
    return setting


def i_setting(name, i):
    setting = f'{name}({i})\n'
    return setting


def generate_server(server_name, server_password, server_port, internet_server, friendly_fire, public_slots,
                    players_to_start, points_limit_default, bounty_limit_default, time_limit_default):
    settings = [s_setting('ServerName', server_name), s_setting('ServerPassword', server_password),
                i_setting('ServerPort', server_port), '\n', i_setting('InternetServer', internet_server),
                i_setting('FriendlyFire', friendly_fire), i_setting('PublicSlots', public_slots),
                i_setting('PlayersToStart', players_to_start), '\n',
                i_setting('PointsLimitDefault', points_limit_default),
                i_setting('BountyLimitDefault', bounty_limit_default),
                i_setting('TimeLimitDefault', time_limit_default), '\n']
    return settings


def get_map_pool(use_custom_maps):
    map_pool = [level[0] for level in MAPS]
    if use_custom_maps:
        map_pool.extend([level[0] for level in CUSTOM_MAPS])
    return map_pool


def get_mode_pool(modes):
    mode_pool = []
    for mode in modes:
        if mode not in mode_pool:
            mode_pool.append(mode)
    return mode_pool


def generate_map_tuples(map_pool, mode_pool):
    map_tuples = []
    for mode in mode_pool:
        for level in map_pool:
            map_tuples.append((level, mode))
    return map_tuples


def generate_mode(args, modes):
    settings = []
    for mode in modes:
        if mode != 'historical':
            if mode == 'teamwanted':
                if args.points_limit:
                    settings.append(si_setting('PointsLimit', mode, args.points_limit))
            else:
                if args.bounty_limit:
                    settings.append(si_setting('BountyLimit', mode, args.bounty_limit))
            if args.time_limit:
                settings.append(si_setting('TimeLimit', mode, args.time_limit))
    return settings


def generate_levels(map_tuples, limit):
    settings = []
    random.seed()
    random.shuffle(map_tuples)
    for level in map_tuples[:limit]:
        settings.append(ss_setting('Map', level[0], level[1]))
    return settings


def generate_file(args):
    settings = []
    settings.extend(generate_server(args.server_name, args.server_password, args.server_port, args.internet_server,
                                    args.friendly_fire,
                                    args.public_slots, args.players_to_start, args.points_limit_default,
                                    args.bounty_limit_default,
                                    args.time_limit_default))
    map_pool = get_map_pool(args.custom_maps)
    mode_pool = get_mode_pool(args.modes)
    map_tuples = generate_map_tuples(map_pool, mode_pool)
    settings.extend(generate_mode(args, map_tuples))
    settings.extend(generate_levels(map_tuples, args.map_limit))
    return settings


def print_settings(settings):
    for line in settings:
        print(line, end='')


def write_settings(settings, file_name):
    with open(file_name, 'w') as file:
        for line in settings:
            file.write(line)


def main():
    parser = get_parser()
    args = parse_args(parser)
    settings = generate_file(args)
    print_settings(settings)
    write_settings(settings, args.output_file)


if __name__ == "__main__":
    main()
