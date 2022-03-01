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
OUTPUT_FILE = 'DedicatedServerSettings.ini'


def strip_arr(arr, pos):
    new_arr = []
    for i in arr:
        new_arr.append(i[pos])
    return new_arr


def get_parser(version='0.69'):
    parser = argparse.ArgumentParser(description='Generate a DedicatedServerSettings.ini for CoJ2')
    parser.add_argument('--internet_server', dest='internet_server', type=int, default=0, choices=[0, 1],
                        help='1 means internet server, 0 means LAN server')
    parser.add_argument('--public_slots', dest='public_slots', type=int, default=12,
                        help='number of public slots (max players), 12 by default')
    parser.add_argument('--players_to_start', dest='players_to_start', type=int, default=1,
                        help='minimum number of players for the game to begin, 1 by default')
    parser.add_argument('--points_limit_default', dest='points_limit_default', type=int, default=10,
                        help='target number of points for the game to end (for "teamwanted" only)')
    parser.add_argument('--bounty_limit_default', dest='bounty_limit_default', type=int, default=1000,
                        help='target of bounty for the game to end (for "wanted", "deathmatch", "teamdeathmatch" only)')
    parser.add_argument('--time_limit_default', dest='time_limit_default', type=int, default=1200,
                        help='map time limit in seconds (for "teamwanted", "wanted", "deathmatch", "teamdeathmatch" only)')
    parser.add_argument('--points_limit', dest='points_limit', type=int,
                        help='target number of points for the game to end in game mode s (for "teamwanted" only)')
    parser.add_argument('--bounty_limit', dest='bounty_limit', type=int,
                        help='target of bounty for the game to end in game modes (for "wanted", "deathmatch", "teamdeathmatch" only)')
    parser.add_argument('--time_limit', dest='time_limit', type=int,
                        help='map time limit in seconds in game mode s (for "teamwanted", "wanted", "deathmatch", "teamdeathmatch" only)')
    parser.add_argument('--friendly_fire', dest='friendly_fire', type=int, default=1, choices=[0, 1],
                        help='1 = friendly fire is on 0 = friendly fire is off')
    parser.add_argument('--server_name', dest='server_name', default='Krampus in da House',
                        help='server name visible on the server list')
    parser.add_argument('--server_password', dest='server_password', default='',
                        help='password for starting the server - should be defined to prevent other servers from using the same name')
    parser.add_argument('--server_port', dest='server_port', type=int, default=27632,
                        help='port the server is running on')
    parser.add_argument('--mode', dest='mode', default='deathmatch', choices=strip_arr(MODES, 0), help='')
    parser.add_argument('--use_custom_maps', dest='use_custom_maps', default=False,
                        action=argparse.BooleanOptionalAction, help='')
    parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version))
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


def generate_server(args, file):
    file.write(s_setting('ServerName', args.server_name))
    file.write(s_setting('ServerPassword', args.server_password))
    file.write(i_setting('ServerPort', args.server_port))
    file.write('\n')
    file.write(i_setting('InternetServer', args.internet_server))
    file.write(i_setting('FriendlyFire', args.friendly_fire))
    file.write(i_setting('PublicSlots', args.public_slots))
    file.write(i_setting('PlayersToStart', args.players_to_start))
    file.write('\n')
    file.write(i_setting('PointsLimitDefault', args.points_limit_default))
    file.write(i_setting('BountyLimitDefault', args.bounty_limit_default))
    file.write(i_setting('TimeLimitDefault', args.time_limit_default))
    file.write('\n')


def generate_mode(args, file):
    if args.mode != 'historical':
        if args.mode == 'teamwanted':
            if args.points_limit:
                file.write(si_setting('PointsLimit', args.mode, args.points_limit))
        else:
            if args.bounty_limit:
                file.write(si_setting('BountyLimit', args.mode, args.bounty_limit))
        if args.time_limit:
            file.write(si_setting('TimeLimit', args.mode, args.time_limit))


def generate_levels(args, file):
    map_list = MAPS
    if args.use_custom_maps:
        for level in CUSTOM_MAPS:
            map_list.append(level)
    random.seed()
    random.shuffle(map_list)
    for level in map_list:
        file.write(ss_setting('Map', level[0], args.mode))


def generate_file(args):
    out_file = open(OUTPUT_FILE, 'w')
    generate_server(args, out_file)
    generate_mode(args, out_file)
    generate_levels(args, out_file)
    out_file.close()


def main():
    parser = get_parser()
    args = parse_args(parser)
    generate_file(args)


if __name__ == "__main__":
    main()
