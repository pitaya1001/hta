# Look at the end to see real outputs

from sa.samp import *
from socket import *

ADDR = ('127.0.0.1', 7777)
RCON_PASSWORD = 'changeme'

s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(1)

def print_queries():
    try:
        while True:
            data, addr = s.recvfrom(2**16)
            try:
                print(Query.decode_response(data))
            except: # bad query response
                pass
    except TimeoutError:
        pass
    print() # blank separator

if __name__ == '__main__':
    # Test ping query
    q = PingQueryRequest(ADDR[0], ADDR[1], 12345678)
    print(q)
    s.sendto(q.encode(), ADDR)
    print_queries()

    # Test info query
    q = InfoQueryRequest(ADDR[0], ADDR[1])
    print(q)
    s.sendto(q.encode(), ADDR)
    print_queries()

    # Test rules query
    q = RulesQueryRequest(ADDR[0], ADDR[1])
    print(q)
    s.sendto(q.encode(), ADDR)
    print_queries()

    # Test clients query
    q = ClientsQueryRequest(ADDR[0], ADDR[1])
    print(q)
    s.sendto(q.encode(), ADDR)
    print_queries()

    # Test detailed players query
    q = DetailedQueryRequest(ADDR[0], ADDR[1])
    print(q)
    s.sendto(q.encode(), ADDR)
    print_queries()

    # Test multiple rcon queries
    for cmd in ['varlist', 'players', 'cmdlist']:
        # Test rcon query (varlist)
        q = RconQueryRequest(ADDR[0], ADDR[1], RCON_PASSWORD, cmd)
        print(q)
        s.sendto(q.encode(), ADDR)
        print_queries()


''' Expected output on default samp-server.exe(assuming there is one player named 'Bob')
C:\dev\hta\examples>query.py
<PingQueryRequest ip='127.0.0.1' port=7777 time=12345678>
<PingQueryResponse ip='127.0.0.1' port=7777 time=12345678>

<InfoQueryRequest ip='127.0.0.1' port=7777>
<InfoQueryResponse ip='127.0.0.1' port=7777 has_password=False player_count=1 max_player_count=50 hostname='SA-MP 0.3 Server' gamemode='Rivershell' language='English'>

<RulesQueryRequest ip='127.0.0.1' port=7777>
<RulesQueryResponse ip='127.0.0.1' port=7777 rules=[('lagcomp', 'On'), ('mapname', 'San Andreas'), ('version', '0.3.7'), ('weather', '11'), ('weburl', 'www.sa-mp.com'), ('worldtime', '12:00')]>

<ClientsQueryRequest ip='127.0.0.1' port=7777>
<ClientsQueryResponse ip='127.0.0.1' port=7777 clients=[('bob', 0)]>

<DetailedQueryRequest ip='127.0.0.1' port=7777>
<DatailedQueryResponse ip='127.0.0.1' port=7777 players=[(0, 'bob', 0, 11)]>

<RconQueryRequest ip='127.0.0.1' port=7777 password='123' command='varlist'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='Console Variables:'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  ackslimit\t= 3000  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  announce\t= 0  (bool)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  bind\t\t= ""  (string) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  chatlogging\t= 0  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  connseedtime\t= 300000  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  filterscripts\t= "gl_actions"  (string) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode0\t= "rivershell"  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode1\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode10\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode11\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode12\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode13\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode14\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode15\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode2\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode3\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode4\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode5\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode6\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode7\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode8\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemode9\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gamemodetext\t= "Rivershell"  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gravity\t= "0.008"  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  hostname\t= "SA-MP 0.3 Server"  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  incar_rate\t= 40  (int) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  lagcomp\t= "On"  (string) (read-only) (rule)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  lagcompmode\t= 1  (int) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  language\t= "English"  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  lanmode\t= 0  (bool)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  logqueries\t= 0  (bool)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  logtimeformat\t= "[%H:%M:%S]"  (string) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  mapname\t= "San Andreas"  (string) (rule)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  maxnpc\t= 0  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  maxplayers\t= 50  (int) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  messageholelimit\t= 3000  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  messageslimit\t= 500  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  minconnectiontime\t= 0  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  myriad\t= 0  (bool)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  nosign\t= ""  (string) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  onfoot_rate\t= 40  (int) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  password\t= ""  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  playertimeout\t= 10000  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  plugins\t= ""  (string) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  port\t\t= 7777  (int) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  query\t\t= 1  (bool)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  rcon\t\t= 1  (bool)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  rcon_password\t= "123"  (string)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  sleep\t\t= 5  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  stream_distance\t= 300.000000  (float)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  stream_rate\t= 1000  (int)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  timestamp\t= 1  (bool)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  version\t= "0.3.7"  (string) (read-only) (rule)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  weapon_rate\t= 40  (int) (read-only)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  weather\t= "11"  (string) (rule)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  weburl\t= "www.sa-mp.com"  (string) (rule)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  worldtime\t= "12:00"  (string) (rule)'>
<RconQueryResponse ip='127.0.0.1' port=7777 response=''>

<RconQueryRequest ip='127.0.0.1' port=7777 password='123' command='players'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='ID\tName\tPing\tIP'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='0\tbob\t11\t127.0.0.1'>

<RconQueryRequest ip='127.0.0.1' port=7777 password='123' command='cmdlist'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='Console Commands:'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  echo'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  exec'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  cmdlist'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  varlist'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  exit'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  kick'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  ban'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gmx'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  changemode'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  say'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  reloadbans'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  reloadlog'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  players'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  banip'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  unbanip'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  gravity'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  weather'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  loadfs'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  unloadfs'>
<RconQueryResponse ip='127.0.0.1' port=7777 response='  reloadfs'>
<RconQueryResponse ip='127.0.0.1' port=7777 response=''>

C:\dev\hta\examples>
'''








''' Test output on (193.84.90.20:7777)
C:\dev\hta\examples>query.py
<PingQueryRequest ip='193.84.90.20' port=7777 time=12345678>
<PingQueryResponse ip='193.84.90.20' port=7777 time=12345678>

<InfoQueryRequest ip='193.84.90.20' port=7777>
<InfoQueryResponse ip='193.84.90.20' port=7777 has_password=False player_count=57 max_player_count=200 hostname='Monser DM | Server 02' gamemode='Monser DM && TDM' language='Russian/English'>

<RulesQueryRequest ip='193.84.90.20' port=7777>
<RulesQueryResponse ip='193.84.90.20' port=7777 rules=[('lagcomp', 'On'), ('mapname', 'Ghetto'), ('version', '0.3.7-R2'), ('weather', '23'), ('weburl', 'monser.ru'), ('worldtime', '12:00')]>

<ClientsQueryRequest ip='193.84.90.20' port=7777>
<ClientsQueryResponse ip='193.84.90.20' port=7777 clients=[('[GW]Tomik_Warrior', 22), ('[GW]Casey_Morton', 6904), ('[DM]oishu.incrible', 21557), ('[GW]Evan_Bexterr', 11), ('[DM]Qwary_Flays', 35), ('[DM]Declan_Follou', 2620), ('[DM]PlotnoKalit', 5513), ('[DM]Seth_Winston', 7530), ('[DM]Fedya_Francesca', 20), ('[TS]Feramon_Dushi', 19), ('[DM]Getto_tascher', 1359), ('[DM]vinobozz', 17), ('[DM]Andrei_Sundin', 6800), ('[DM]Dreikee.Frequency', 97), ('[TS]Jeff_Dahmer', 75), ('[DM]Dolinka_Egora', 9), ('[TS]priora_hasaviurt', 43), ('[GW]chin.vagner', 573), ('[GW]Gashik.', 22241), ('[DM]chrome_google', 52), ('[TS]sunset.earldom', 12053), ('[TS]Jonathan_Monter', 3), ('[DM]Nester_kown', 108), ('[DM]gjfk_fds', 19), ('[GW]cho_jail', 4866), ('[DM]Your_Tyanka', 43), ('[TS]texa', 136), ('[DM]Nik_Angels', 5615), ('[DM]Dima_Yakyzayaex', 11), ('[GW]Cheater_Softerias', 24952), ('[DM]Bimba_Zabivnoi', 5), ('[GW]Jey_Fram', 8857), ('[DM]Kirya_Pinaev', 573), ('[DM]Serka', 32137), ('[DM]Side_Black', 76), ('[DM]Soul_Morris', 138), ('[DM]123y763147685234', 72), ('[DM]abduqawindai', 0), ('[DM]vasyavasya', 12), ('[TS]Maksim_Kartochova', 0), ('[TS]Amoral_Outcast', 436), ('[DM]Zenya_Kamazov', 10160), ('[TS]Operator_Capton', 1307), ('[DM]Muichiro_Supler', 648), ('[DM]best.super.best', 201), ('[DM]Nathan_Defender', 2052), ('[DM]Archangel', 423), ('[TS]reallG', 3), ('[DM]Warmer_Legendary', 512), ('[TS]Xeon_Gold', 1394), ('dfsdffsdfdfffffszzz', 0), ('[DM]nodomesu', 0), ('[MM]Killua_', 0), ('[MM]Killua_Ebet', 0), ('[GW]Tommie_Desperete', 294), ('[DM]Ricko_Radrigges', 21287), ('[DM]Kostik_Tripovzzzzzzz', 264)]>

<DetailedQueryRequest ip='193.84.90.20' port=7777>
<DatailedQueryResponse ip='193.84.90.20' port=7777 players=[(0, '[GW]Tomik_Warrior', 22, 117), (1, '[GW]Casey_Morton', 6904, 95), (2, '[DM]oishu.incrible', 21557, 128), (3, '[GW]Evan_Bexterr', 11, 81), (4, '[DM]Qwary_Flays', 35, 74), (5, '[DM]Declan_Follou', 2620, 84), (6, '[DM]PlotnoKalit', 5513, 95), (7, '[DM]Seth_Winston', 7530, 106), (8, '[DM]Fedya_Francesca', 20, 56), (9, '[TS]Feramon_Dushi', 19, 92), (10, '[DM]Getto_tascher', 1359, 132), (11, '[DM]vinobozz', 17, 151), (12, '[DM]Andrei_Sundin', 6800, 81), (13, '[DM]Dreikee.Frequency', 97, 114), (14, '[TS]Jeff_Dahmer', 75, 114), (15, '[DM]Dolinka_Egora', 9, 122), (16, '[TS]priora_hasaviurt', 43, 75), (17, '[GW]chin.vagner', 573, 78), (18, '[GW]Gashik.', 22241, 98), (19, '[DM]chrome_google', 52, 148), (20, '[TS]sunset.earldom', 12053, 55), (21, '[TS]Jonathan_Monter', 3, 123), (22, '[DM]Nester_kown', 108, 85), (23, '[DM]gjfk_fds', 19, 154), (24, '[GW]cho_jail', 4866, 130), (25, '[DM]Your_Tyanka', 43, 58), (26, '[TS]texa', 136, 112), (27, '[DM]Nik_Angels', 5615, 76), (28, '[DM]Dima_Yakyzayaex', 11, 68), (29, '[GW]Cheater_Softerias', 24952, 81), (30, '[DM]Bimba_Zabivnoi', 5, 78), (31, '[GW]Jey_Fram', 8857, 165), (32, '[DM]Kirya_Pinaev', 573, 63), (33, '[DM]Serka', 32138, 104), (34, '[DM]Side_Black', 76, 101), (35, '[DM]Soul_Morris', 138, 88), (36, '[DM]123y763147685234', 72, 95), (37, '[DM]abduqawindai', 0, 98), (38, '[DM]vasyavasya', 12, 84), (39, '[TS]Maksim_Kartochova', 0, 136), (40, '[TS]Amoral_Outcast', 436, 70), (41, '[DM]Zenya_Kamazov', 10160, 71), (42, '[TS]Operator_Capton', 1307, 138), (43, '[DM]Muichiro_Supler', 648, 64), (44, '[DM]best.super.best', 201, 114), (45, '[DM]Nathan_Defender', 2052, 149), (46, '[DM]Archangel', 423, 91), (47, '[TS]reallG', 3, 74), (48, '[DM]Warmer_Legendary', 512, 87), (49, '[TS]Xeon_Gold', 1394, 87), (51, 'dfsdffsdfdfffffszzz', 0, 161), (52, '[DM]nodomesu', 0, 76), (53, '[MM]Killua_', 0, 86), (54, '[MM]Killua_Ebet', 0, 122), (56, '[GW]Tommie_Desperete', 294, 81), (57, '[DM]Ricko_Radrigges', 21287, 84), (76, '[DM]Kostik_Tripovzzzzzzz', 264, 58)]>

<RconQueryRequest ip='193.84.90.20' port=7777 password='123' command='varlist'>
<RconQueryResponse ip='193.84.90.20' port=7777 response='Invalid RCON password.'>

<RconQueryRequest ip='193.84.90.20' port=7777 password='123' command='players'>
<RconQueryResponse ip='193.84.90.20' port=7777 response='Invalid RCON password.'>

<RconQueryRequest ip='193.84.90.20' port=7777 password='123' command='cmdlist'>
<RconQueryResponse ip='193.84.90.20' port=7777 response='Invalid RCON password.'>


C:\dev\hta\examples>
'''
