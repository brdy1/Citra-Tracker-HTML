import struct
import time
import os
import subprocess
import json
import sqlite3
import threading
import traceback
from configparser import ConfigParser
from datetime import datetime
from citra import Citra


def crypt(data, seed, i):
    value = data[i]
    shifted_seed = seed >> 16
    shifted_seed &= 0xFF
    value ^= shifted_seed
    result = struct.pack("B", value)

    value = data[i + 1]
    shifted_seed = seed >> 24
    shifted_seed &= 0xFF
    value ^= shifted_seed
    result += struct.pack("B", value)

    return result

def crypt_array(data, seed, start, end):
    result = bytes()
    temp_seed = seed

    for i in range(start, end, 2):
        temp_seed *= 0x41C64E6D
        temp_seed &= 0xFFFFFFFF
        temp_seed += 0x00006073
        temp_seed &= 0xFFFFFFFF
        result += crypt(data, temp_seed, i)

    return result

def shuffle_array(data, sv, block_size):
    block_position = [[0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 2, 3, 1, 1, 2, 3, 2, 3, 1, 1, 2, 3, 2, 3],
                      [1, 1, 2, 3, 2, 3, 0, 0, 0, 0, 0, 0, 2, 3, 1, 1, 3, 2, 2, 3, 1, 1, 3, 2],
                      [2, 3, 1, 1, 3, 2, 2, 3, 1, 1, 3, 2, 0, 0, 0, 0, 0, 0, 3, 2, 3, 2, 1, 1],
                      [3, 2, 3, 2, 1, 1, 3, 2, 3, 2, 1, 1, 3, 2, 3, 2, 1, 1, 0, 0, 0, 0, 0, 0]]
    result = bytes()
    for block in range(4):
        start = block_size * block_position[block][sv]
        end = start + block_size
        result += data[start:end]
    return result

def decrypt_data(encrypted_data):
    pv = struct.unpack("<I", encrypted_data[:4])[0]
    sv = ((pv >> 0xD) & 0x1F) % 24

    start = 8
    end = (4 * BLOCK_SIZE) + start

    header = encrypted_data[:8]

    # Blocks
    blocks = crypt_array(encrypted_data, pv, start, end)

    # Stats
    stats = crypt_array(encrypted_data, pv, end, len(encrypted_data))

    final_result = header + shuffle_array(blocks, sv, BLOCK_SIZE) + stats

    return final_result

class Pokemon:
    def __init__(self, encrypted_data):
        first_byte = encrypted_data[0]
        if first_byte != 0:
            self.raw_data = decrypt_data(encrypted_data)
        else:
            self.raw_data = ""

    def species_num(self):
        if len(self.raw_data) > 0:
            return struct.unpack("<H", self.raw_data[0x8:0xA])[0]
        else:
            return 0

    def getAtts(self,gamegroupid,gen):
        dex = self.species_num()
        form = struct.unpack("B",self.raw_data[0x1D:0x1E])[0]
        query = f"""select pokemonid from "pokemon.pokemon" where pokemonpokedexnumber = {dex}"""
        match dex:
            case 81 | 82 | 100 | 101 | 120 | 121 | 137 | 233 | 292 | 337 | 338 | 343 | 344 | 374 | 375 | 376 | 436 | 437 | 462 | 474 | 489 | 490 | 599 | 600 | 601 | 615 | 622 | 623 | 703 | 774 | 781 | 854 | 855 | 770 | 132 | 144 | 145 | 146 | 201 | 243 | 244 | 245 | 249 | 250 | 251 | 377 | 378 | 379 | 382 | 383 | 384 | 385 | 386 | 480 | 481 | 482 | 483 | 484 | 486 | 491 | 493 | 494 | 638 | 639 | 640 | 643 | 644 | 646 | 647 | 649 | 716 | 717 | 718 | 719 | 721: ### Genderless exceptions
                query+= " and pokemonsuffix is null"
            case 641 | 642 | 645:
                if form > 0: ### Therian forms of Tornadus, Thundurus, Landorus
                    query+= " and pokemonsuffix = 'therian"
            case 6:
                match form:
                    case 8 | 10:
                        query+= " and pokemonsuffix = 'mega-x'"
                    case 16 | 18:
                        query+= " and pokemonsuffix = 'mega-y'"
            case 150: ### Mewtwo
                match form:
                    case 12:
                        query+= " and pokemonsuffix = 'mega-x'"
                    case 20: ### Mewtwo Y
                        query+= " and pokemonsuffix = 'mega-y'"
            case 351: ### Castform
                match form:
                    case 8 | 10:
                        query+= " and pokemonsuffix = 'sunny'"
                    case 16 | 18:
                        query+= " and pokemonsuffix = 'rainy'"
                    case 24 | 26:
                        query+= " and pokemonsuffix = 'snowy'"
            case 386: ### Deoxys
                match form:
                    case 12:
                        query+= " and pokemonsuffix = 'attack'"
                    case 20:
                        query+= " and pokemonsuffix = 'defense'"
                    case 28:
                        query+= " and pokemonsuffix = 'speed'"
            case 413: ### Wormadam
                match form:
                    case 10:
                        query+= " and pokemonsuffix = 'sandy'"
                    case 18:
                        query+= " and pokemonsuffix = 'trash'"
                    case 2:
                        query+= " and pokemonsuffix = 'plant'"
            case 479: ### Rotom
                match form:
                    case 12:
                        query+= " and pokemonsuffix = 'heat'"
                    case 20:
                        query+= " and pokemonsuffix = 'wash'"
                    case 28:
                        query+= " and pokemonsuffix = 'frost'"
                    case 36:
                        query+= " and pokemonsuffix = 'fan'"
                    case 44:
                        query+= " and pokemonsuffix = 'mow'"
            case 487: ### Giratina
                match form:
                    case 12:
                        query+= " and pokemonsuffix = 'origin'"
            case 492: ### Shaymin
                match form:
                    case 12:
                        query+= " and pokemonsuffix = 'sky'"
            case 555: ### Darmanitan
                match form:
                    case 8 | 10:
                        query+= " and pokemonsuffix = 'zen'"
            case 648: ### Meloetta
                match form:
                    case 12:
                        query+= " and pokemonsuffix = 'pirouette'"
                    case 4:
                        query+= " and pokemonsuffix = 'aria'"
            case 646: ### Kyurem
                match form:
                    case 12:
                        query+= " and pokemonsuffix = 'white'"
                match form:
                    case 20:
                        query+= " and pokemonsuffix = 'black'"
            case 670: ### Floette
                match form:
                    case 18:
                        query+= " and pokemonsuffix = 'eternal'"
            case 678: ### Meowstic
                match form:
                    case 10:
                        query+= " and pokemonsuffix = 'f'"
            case 681: ### Aegislash
                match form:
                    case 0 | 2:
                        query+= " and pokemonsuffix = 'shield'"
                    case 8 | 10:
                        query+= " and pokemonsuffix = 'blade'"
            # case 718: ### Zygarde only needed for gen 7
            #     print(form)
            # case 720: ### Hoopa
            #     print(form)
            # case 741: ### Oricorio
            #     print(form)
            # case 745: ### Lycanroc
            #     print(form)
            # case 746: ### Wishiwashi
            #     print(form)
            # case 774: ### Minior
            #     print(form)
            # case 800: ### Necrozma
            #     print(form)
            case _:
                if form == 2:
                    query+= " and pokemonsuffix is null"
                elif form > 0:
                    query+= " and pokemonsuffix ='mega'"
                else:
                    query+= " and pokemonsuffix is null"
        # print(form)
        # print(query)
        self.id = cursor.execute(query).fetchone()[0]
        self.species,self.suffix,self.name = cursor.execute(f"""select pokemonspeciesname,pokemonsuffix,pokemonname from "pokemon.pokemon" where pokemonid = {self.id}""").fetchone()
        self.suffix = self.suffix or ''
        self.name = self.name.replace(' Form','').replace(' Cloak','')
        self.spritename = self.species.lower()+('' if self.suffix == '' else ('-'+self.suffix))
        self.spriteurl = "https://img.pokemondb.net/sprites/"+getURLAbbr(gamegroupid)+"/normal/"+self.spritename+".png"
        self.bst = cursor.execute(f"""select
                                sum(pokemonstatvalue)
                            from "pokemon.pokemonstat"
                                where pokemonid = {self.id}
                                and generationid = (
                                    select
                                        max(generationid)
                                    from "pokemon.pokemonstat"
                                        where generationid <= {gen}
                                )""").fetchone()[0]    
        self.types = cursor.execute(f"""
                               select
                                    ty.typename
                                from "pokemon.pokemontype" pt
                                    left join "pokemon.type" ty on pt.typeid = ty.typeid
                                where pt.pokemonid = {self.id} and pt.generationid = {gen}                              
                               """).fetchall()
        self.types = [type for type in self.types]
        self.held_item_name = items[str(struct.unpack("<H", self.raw_data[0xA:0xC])[0])]['name'].replace("é","&#233;")
        self.ability_num = struct.unpack("B", self.raw_data[0x14:0x15])[0] # Ability
        query = f"""select
                        ab.abilityname
                        ,abilitydescription
                    from "pokemon.generationability" ga
                        left join "pokemon.ability" ab on ga.abilityid = ab.abilityid
                        left join "pokemon.abilitylookup" al on ab.abilityname = al.abilityname
                    where al.abilityindex = {self.ability_num} and ga.generationid <= {gen}
                    order by ga.generationid desc
                    """
        self.abilityname,self.abilitydescription = cursor.execute(query).fetchone()
        self.ability = {'name':self.abilityname,'description':self.abilitydescription}
        self.nature_num = struct.unpack("B", self.raw_data[0x1C:0x1D])[0] ## Nature
        self.nature = cursor.execute(f"""select
                        n.naturename
                    from "pokemon.nature" n
                        left join "pokemon.naturelookup" nl on n.naturename = nl.naturename
                    where nl.natureindex = {self.nature_num}
                    """).fetchone()[0]
        self.friendship = struct.unpack("B", self.raw_data[0xCA:0xCB])[0] ### Friendship
        self.level_met = struct.unpack("<H", self.raw_data[0xDD:0xDF])[0] ####### Level met
        self.level = struct.unpack("B", self.raw_data[0xEC:0xED])[0] ### Current level
        self.cur_hp = struct.unpack("<H", self.raw_data[0xF0:0xF2])[0] ####### Current HP
        self.maxhp = struct.unpack("<H", self.raw_data[0xF2:0xF4])[0] ## Max HP
        self.attack = struct.unpack("<H", self.raw_data[0xF4:0xF6])[0] ## Attack stat
        self.defense = struct.unpack("<H", self.raw_data[0xF6:0xF8])[0] ## Defense stat
        self.speed = struct.unpack("<H", self.raw_data[0xF8:0xFA])[0] ## Speed stat
        self.spatk = struct.unpack("<H", self.raw_data[0xFA:0xFC])[0] ## Special attack stat
        self.spdef = struct.unpack("<H", self.raw_data[0xFC:0xFE])[0] ## Special defense stat
        self.evhp = struct.unpack("B", self.raw_data[0x1E:0x1F])[0]
        self.evattack = struct.unpack("B", self.raw_data[0x1F:0x20])[0]
        self.evdefense = struct.unpack("B", self.raw_data[0x20:0x21])[0]
        self.evspeed = struct.unpack("B", self.raw_data[0x21:0x22])[0]
        self.evspatk = struct.unpack("B", self.raw_data[0x22:0x23])[0]
        self.evspdef = struct.unpack("B", self.raw_data[0x23:0x24])[0]
        self.ivloc = struct.unpack("<I", self.raw_data[0x74:0x78])[0]
        self.ivhp = (self.ivloc >> 0) & 0x1F ############################## HP IV
        self.ivattack = (self.ivloc >> 5) & 0x1F ############################## Attack IV
        self.ivdefense = (self.ivloc >> 10) & 0x1F ############################# Defense IV
        self.ivspeed = (self.ivloc >> 15) & 0x1F ############################# Speed IV
        self.ivspatk = (self.ivloc >> 20) & 0x1F ############################# Special attack IV
        self.ivspdef = (self.ivloc >> 25) & 0x1F ############################# Special defense IV
        def moves(self):
                def movedescription(id):
                    query = f"""select movedescription from "pokemon.generationmove" where generationmoveid = {id}"""
                    return cursor.execute(query).fetchone()[0]
                move1 = ((0x5A,0x5C),(0x62,0x63))
                move2 = ((0x5C,0x5E),(0x63,0x64))
                move3 = ((0x5E,0x60),(0x64,0x65))
                move4 = ((0x60,0x62),(0x65,0x66))
                for ml,pl in (move1,move2,move3,move4):
                    try:
                        move_num = struct.unpack("<H", self.raw_data[ml[0]:ml[1]])[0]
                        query = f"""
                            select
                                mv.movename,
                                gm.generationmoveid,
                                movepp,
                                typename,
                                movepower,
                                moveaccuracy,
                                movecontactflag,
                                movecategoryname
                            from "pokemon.generationmove" gm
                                left join "pokemon.move" mv on gm.moveid = mv.moveid
                                left join "pokemon.movelookup" ml on mv.movename = ml.movename
                                left join "pokemon.type" ty on gm.typeid = ty.typeid
                                left join "pokemon.movecategory" mc on gm.movecategoryid = mc.movecategoryid
                            where ml.moveindex = {move_num} and gm.generationid = {gen}"""
                        movename,id,pp,type,power,acc,contact,category = cursor.execute(query).fetchone()
                        yield {'name':movename,
                            'description':movedescription(id),
                                'pp':struct.unpack("<B",self.raw_data[pl[0]:pl[1]])[0],
                                'maxpp':int(pp),
                                'type':type,
                                'power':power,
                                'acc':acc,
                                'contact':contact,
                                'category':category
                            }
                    except:
                        yield {'name':'',
                               'description':'',
                               'pp':0,
                               'maxpp':0,
                                'type':None,
                                'power':0,
                                'acc':0,
                                'contact':False,
                                'category':None}
                    
        self.moves = [move for move in moves(self)]
        try:
            self.evotype,self.evoitem,self.evolevel,self.evostring,self.evolocation = cursor.execute(f"""
                                            SELECT
                                                evolutiontypename,
                                                itemname,
                                                pokemonevolutionlevel,
                                                pokemonevolutionuniquestring,
                                                locationname
                                            FROM "pokemon.pokemonevolutioninfokaizo" peik
                                                LEFT JOIN "pokemon.item" it ON peik.itemid = it.itemid
                                                LEFT JOIN "pokemon.pokemon" target ON peik.targetpokemonid = target.pokemonid
                                                LEFT JOIN "pokemon.evolutiontype" evot ON peik.evolutiontypeid = evot.evolutiontypeid
                                                LEFT JOIN "pokemon.location" loc ON peik.locationid = loc.locationid
                                                WHERE gamegroupid IN (
                                                    SELECT
                                                        gamegroupid
                                                    FROM "pokemon.gamegroup"
                                                        WHERE gamegrouporder < (
                                                            SELECT
                                                                gamegrouporder
                                                            FROM "pokemon.gamegroup"
                                                                WHERE gamegroupid = '{gamegroupid}'
                                                            )
                                                    )
                                                AND basepokemonid = {str(self.id)}
            """).fetchone()
            self.evo = True
        except:
            self.evo = False
        self.statusbyte = struct.unpack("<B",self.raw_data[0xE8:0xE9])[0] ### Status byte
        match self.statusbyte:
            case 1:
                self.status = 'Paralyzed'
            case 2:
                self.status = 'Asleep'
            case 3:
                self.status = 'Frozen'
            case 4:
                self.status = 'Burned'
            case 5:
                self.status = 'Poisoned'
            case _:
                self.status = ''
        
    def getStatChanges(self):
            raised,lowered = cursor.execute(f"""
            select
                    raisedstat.statname
                    ,loweredstat.statname
                from "pokemon.nature" n
                    left join "pokemon.stat" raisedstat on n.raisedstatid = raisedstat.statid
                    left join "pokemon.stat" loweredstat on n.loweredstatid = loweredstat.statid
                where n.naturename = '{self.nature}'
                """).fetchone()
            for stat in ('Attack','Defense','Special Attack','Special Defense','Speed'):
                if stat == raised:
                    yield 'raised'
                elif stat == lowered:
                    yield 'lowered'
                else:
                    yield ''

    def getMoves(self,gamegroupid):
        learnedcount = 0
        query = f"""
            select
                pokemonmovelevel
            from "pokemon.pokemonmove" pm
                left join "pokemon.pokemonmovemethod" pmm on pm.pokemonmovemethodid = pmm.pokemonmovemethodid
                where gamegroupid = {gamegroupid}
                    and pokemonmovemethodname = 'Level up'
                    and pokemonmovelevel > 1
                    and pokemonid = {self.id}
                order by pokemonmovelevel
        """
        learnlist = cursor.execute(query).fetchall()
        nextmove = None
        totallearn = 0
        learnstr = ''
        for learn in learnlist:
            learnstr+=str(learn[0])+', '
            if int(learn[0]) > 1:
                totallearn+=1
        for learn in learnlist:
            if not int(learn[0]) <= int(self.level):
                nextmove = learn[0]
                break
            elif int(learn[0]) > 1:
                learnedcount+=1
        return totallearn,nextmove,learnedcount,learnstr[0:len(learnstr)-2]

    def getCoverage(self,gen,gamegroupid):
        types = []
        for move in self.moves:
            if move['power']:
                if move['power'] > 0:
                    types.append(move['type'])
        monTypes = f"""
            with montypes as (
                select distinct
                    mon.pokemonid as pokemonid,
                    type1.typeid as type1id,
                    type2.typeid as type2id,
                    pt1.generationid as gen
                from "pokemon.pokemon" mon
                    join "pokemon.pokemontype" pt1 on mon.pokemonid = pt1.pokemonid and pt1.pokemontypeorder = 1 and pt1.generationid = {gen}
                    left join "pokemon.pokemontype" pt2 on mon.pokemonid = pt2.pokemonid and pt2.pokemontypeorder = 2 and pt2.generationid = {gen}
                    join "pokemon.type" type1 on pt1.typeid = type1.typeid
                    left join "pokemon.type" type2 on pt2.typeid = type2.typeid
                    join "pokemon.gamegroup" gg on pt1.generationid = gg.generationid and gg.gamegroupid = {gamegroupid}
                    join "pokemon.game" gm on gg.gamegroupid = gm.gamegroupid
                    join "pokemon.pokemongameavailability" pga on mon.pokemonid = pga.pokemonid and gm.gameid = pga.gameid and pga.gameid
                    ),
        """
        monbsts = f"""
            monbsts as (
                select
                    ps.pokemonid as pokemonid,
                    mt.type1id,
                    mt.type2id,
                    mt.gen,
                    sum(ps.pokemonstatvalue) as bst
                from "pokemon.pokemonstat" ps
                    join montypes mt on ps.generationid = mt.gen AND ps.pokemonid = mt.pokemonid
                    GROUP BY 1,2,3,4
            ),
        """
        attackingdamage = f"""
            attackingdmg as (
                select
                    mb.pokemonid as pokemonid,
                    mb.type1id as type1id,
                    mb.type2id as type2id,
                    max(tm1.damagemodifier*coalesce(tm2.damagemodifier,1)) as dmgmod
                from monbsts mb
                    join "pokemon.typematchup" tm1 on mb.type1id = tm1.defendingtypeid and tm1.generationid = mb.gen
                    left join "pokemon.typematchup" tm2
                        on mb.type2id = tm2.defendingtypeid
                        and tm1.attackingtypeid = tm2.attackingtypeid
                        and tm2.generationid = mb.gen
                    join "pokemon.type" attackingtype on tm1.attackingtypeid = attackingtype.typeid
                where attackingtype.typename in {str(types).replace('[','(').replace(']',')')}
                group by 1,2,3

            )
        """
        coveragecountsquery = f"""
                select
                    ad.dmgmod,
                    count(ad.pokemonid)
                from attackingdmg ad
                group by 1
                order by 1 asc
        """
        coveragecounts = cursor.execute(monTypes+monbsts+attackingdamage+coveragecountsquery).fetchall()
        # topbstsquery = f"""
        #     select 
        #         mb.bst,
        #         mon.pokemonname
        #     from attackingdmg ad
        #         join monbsts mb on ad.pokemonid = mb.pokemonid
        #         join "pokemon.pokemon" mon on ad.pokemonid = mon.pokemonid
        #     order by ad.dmgmod asc, mb.bst desc limit 10
        # """
        # topbsts = cursor.execute(monTypes+monbsts+attackingdamage+topbstsquery).fetchall()
        return coveragecounts#,topbsts
        

#######################################################################


class Pokemon6(Pokemon):
    def __init__(self, data):
        Pokemon.__init__(self, data)

class Pokemon7(Pokemon):
    def __init__(self, data):
        Pokemon.__init__(self, data)

def getGame():
    config = ConfigParser()
    config.read('config.ini')
    partyaddresses = {
        'X/Y':0x8CE1CE8,
        'OmegaRuby/AlphaSapphire':0x8CF727C,
        'Sun/Moon':0x34195E10,
        'UltraSun/UltraMoon':0x33F7FA44
    }
    game = config['config']['game']
    return game,(partyaddresses[game] or 0)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def read_party(c,party_address):
    party = []    
    for i in range(6):
        read_address = party_address + (i * SLOT_OFFSET)
        party_data = c.read_memory(read_address, SLOT_DATA_SIZE)
        stats_data = c.read_memory(read_address + SLOT_DATA_SIZE + STAT_DATA_OFFSET, STAT_DATA_SIZE)
        if party_data and stats_data:
            data = party_data + stats_data
            try:
                pokemon = Pokemon6(data)
                party.append(pokemon)
            except ValueError:
                traceback.print_exc()
                pass
    return party

def launchHTTP():
    subprocess.run(["python", "-m", "http.server"]) ## Launches a local http server to allow the DOM/Axios requests
    print("Please direct an OBS Browser Source to http://localhost:8000/tracker.html or ./tracker.html")

def print_bits(value):
    binary = bin(value)[2:].zfill(8)
    bits = [bool(int(bit)) for bit in binary]
    print(bits)

def analyze_statuses(self):
    print('begin statuses')
    # print('statuses:', self.statuses)
    print_bits(self.statusbyte)
    # Analyze bit positions
    print('Asleep:', self.asleep)
    print('Poisoned:', self.poisoned)
    print('Burned:', self.burned)
    print('Frozen:', self.frozen())
    print('Paralyzed:', self.paralyzed)
    # print('Toxic:', self.badlypoisoned())
    print('end statuses')

def calcPower(pkmn,move):
    if move['name'] == 'Eruption':
        return int(int(pkmn.cur_hp())/int(pkmn.stat_hp())*150)
    else:
        return ('-' if not move['power'] else int(move['power']))
    
def getURLAbbr(game):
    if game == 15:
        return 'x-y'
    elif game == 16:
        return 'omega-ruby-alpha-sapphire/dex' ## ORAS sprites end in /dex
    else:
        return 'home'

def run():
    game,party_address = getGame()
    gamegroupid,gamegroupabbreviation,gen = cursor.execute(f"""
            select
                gg.gamegroupid
                ,gg.gamegroupabbreviation
                ,gg.generationid
            from "pokemon.gamegroup" gg
            where gamegroupname = '{game}'""").fetchone()
    print('running..')
    threading.Thread(target=launchHTTP).start()
    htmlfile='tracker.html'
    prevhtmltext=''
    try:
        #print('connecting to citra')
        c = Citra()
        #print('connected to citra')
        htmltext=''
        while True:
            try:
                if c.is_connected():
                    #print('reading party')
                    htmltext='<!DOCTYPE html>\r\n<html>\r\n<head>\r\n\t<title>Gen 6 Tracker</title>\r\n'
                    htmltext+='\t<link rel="stylesheet" type="text/css" href="tracker.css">\r\n</head>\r\n<body>'
                    party = read_party(c,party_address)
                    pk=0
                    #print('read party... performing loop')
                    htmltext+='<div id="party">\r\n'
                    for pkmn in party:
                        if pkmn.species_num() != 0: ### Make sure the slot is valid & not an egg
                            pkmn.getAtts(gamegroupid,gen)
                            if int(pkmn.cur_hp) > 5000: ### Make sure the memory dump hasn't happened (or whatever causes the invalid values)
                                continue
                            if pkmn.species_num() > 1000: ### Make sure the memory dump hasn't happened (or whatever causes the invalid values)
                                continue
                            pk=pk+1
                            # print('unknown flags')
                            # print_bits(pkmn.alt_form)
                            # print_bits(pkmn.unknown_flags_ea())
                            # print_bits(pkmn.unknown_flags_eb())
                            # analyze_statuses(pkmn)
                            #### Begin Pokemon div
                            htmltext+='<div class="pokemon">\r\n\t'
                            htmltext+='<div class="pokemon-top-block">\r\n\t'
                            htmltext+='<div class="pokemon-top-left-block">\r\n\t'
                            htmltext+=f'<div class="sprite">\r\n\t<img src="{pkmn.spriteurl}" data-src="{pkmn.spriteurl}" width="80" height="80" alt="{pkmn.name} sprite">\r\n</div>\r\n\t'
                            htmltext+='     <div class="species">\r\n\t\t'
                            htmltext+='         <div class="slot-number">Slot '+str(party.index(pkmn)+1)+'</div>\r\n\t\t'
                            htmltext+='         <div class="species-number">#'+str(pkmn.species_num())+'</div>\r\n\t\t'
                            htmltext+='         <div class="species-name">'+pkmn.name.replace("Farfetchd","Farfetch&#x27;d")+'</div>\r\n'
                            htmltext+='     </div>\r\n' ## close species
                            ##### TYPES, STATS, ABIILITIES, ETC.
                            typestr = '<div class="type">'
                            for type in pkmn.types:
                                typestr+=f'<img src="images/types/{type[0]}.png" height="16" width="18" alt="{type[0]}"><span class="type '+type[0]+' name">'+type[0]+' </span>'
                            typestr+='</div>'
                            htmltext+='<div class="major-stats">\r\n\t'
                            htmltext+=typestr
                            htmltext+='<div class="level-status">'
                            if pkmn.evo:
                                # evotype = ('' if not pkmn.evotype else pkmn.evotype)
                                evoitem = ('' if not pkmn.evoitem else 'w/'+pkmn.evoitem)
                                evofriend = ('' if pkmn.evotype != 'Friendship' else 'w/ high friendship')
                                evolevel = ('' if not pkmn.evolevel else '@ level '+str(int(pkmn.evolevel)))
                                evostring = ('' if not pkmn.evostring else pkmn.evostring)
                                evoloc = ('' if not pkmn.evolocation else 'in '+pkmn.evolocation)
                                evohtml=f'<div class="evoarrow">></div><div class="evo">Evolves {evoitem} {evofriend} {evolevel} {evostring} {evoloc}</div>'
                            else:
                                evohtml=''
                            htmltext+=f'     <div class="level mstat"><span class="level name">Level: </span><span class="level value">'+str(pkmn.level)+f'</span>{evohtml}</div>\r\n\t'
                            if pkmn.status != '':
                                htmltext+='     <div class="status mstat"><img src="images/statuses/'+pkmn.status+'.png" height="25" width="40"></div>'
                            else:
                                htmltext+='     <div class="status mstat"></div>'
                            htmltext+='</div>\r\n' ## Close level-status div
                            htmltext+='</div>\r\n' ## Close major stats div
                            htmltext+='<div class="ability">\r\n\t'
                            htmltext+='     <div class="ability name"><div class="description">'+str(pkmn.ability['description'])+'</div>'+str(pkmn.ability['name'])+'</div>\r\n'
                            htmltext+='</div>\r\n' ## close ability div
                            htmltext+='<div class="nature">\r\n\t'
                            htmltext+=f'     <div class="nature-name">{pkmn.nature}</div>\r\n'
                            htmltext+='</div>\r\n'
                            htmltext+='<div class="held-item">\r\n\t'
                            htmltext+=f'     <div class="held-item-name">{pkmn.held_item_name}</div>\r\n'
                            htmltext+='</div>\r\n'
                            htmltext+='</div>\r\n'
                            htmltext+='<div class="pokemon-top-right-block">'
                            ### STATS ########
                            htmltext+='<div class="stats">\r\n'
                            attackchange,defchange,spatkchange,spdefchange,speedchange = pkmn.getStatChanges()
                            htmltext+=f'     <div class="hp stat"><span class="name">HP: </span><span class="value"><span class="ev">EV: {pkmn.evhp}</span>{pkmn.cur_hp}/{pkmn.maxhp}</span></div>\r\n'
                            htmltext+=f'     <div class="attack stat {attackchange}"><span class="name">Atk:</span><span class="value"><span class="ev">EV: {pkmn.evattack}</span>{pkmn.attack}</span></div>\r\n\t'
                            htmltext+=f'     <div class="def stat {defchange}"><span class="name">Def:</span><span class="value"><span class="ev">EV: {pkmn.evdefense}</span>{pkmn.defense}</span></div>\r\n\t'
                            htmltext+=f'     <div class="spatk stat {spatkchange}"><span class="name">SpAtk:</span><span class="value"><span class="ev">EV: {pkmn.evspatk}</span>{pkmn.spatk}</span></div>\r\n\t'
                            htmltext+=f'     <div class="spdef stat {spdefchange}"><span class="name">SpDef:</span><span class="value"><span class="ev">EV: {pkmn.evspdef}</span>{pkmn.spdef}</span></div>\r\n\t'
                            htmltext+=f'     <div class="speed stat {speedchange}"><span class="name">Speed:</span><span class="value"><span class="ev">EV: {pkmn.evspeed}</span>{pkmn.speed}</span></div>\r\n\t'
                            htmltext+=f'     <div class="bst stat"><span class="name">BST:</span><span class="value">{pkmn.bst}</span></div>\r\n\t'
                            htmltext+='</div>' ## Close stats div
                            htmltext+='</div>' ## Close top right block
                            htmltext+='</div>' ## Close top block
                            htmltext+='<div class="pokemon-bottom-block">\r\n\t'
                            ### MOVES ########
                            totallearn,nextmove,learnedcount,learnstr = pkmn.getMoves(gamegroupid)
                            htmltext+='<div class="moves">\r\n\t'
                            # counts = pkmn.getCoverage(gen,gamegroupid)
                            # countstr = ''
                            # for dmg,count in counts:
                            #     countstr+='<div class="damage-bracket">['+str(dmg)+'x]</div>'
                            #     countstr+='<div class="bracket-count">'+str(count)+'</div>'
                            nmove = (' - ' if not nextmove else nextmove)
                            htmltext+=f'     <div class="move label"><div class="move category label"><div class="learnset">{learnstr}</div>Moves {learnedcount}/{totallearn} ({nmove})</div><div class="move name label"></div><div class="move maxpp label">PP</div><div class="move power label">BP</div><div class="move accuracy label">Acc</div><div class="move contact label">C</div></div>\r\n\t'
                            for move in pkmn.moves:
                                stab = ''
                                for type in pkmn.types:
                                    if move['type'] == type[0]:
                                        stab = move['type']
                                        continue
                                htmltext+=f'     <div class="move">'
                                htmltext+=f'         <div class="move category"><img src="images/categories/{move["category"]}.png" height="13" width="18"></div>'
                                htmltext+=f'         <div class="move name {move["type"]}"><div class="description">{move["description"]}</div>{move["name"]}</div>'
                                htmltext+=f'         <div class="move maxpp">{move["pp"]}/{move["maxpp"]}</div>'
                                movepower = calcPower(pkmn,move)
                                htmltext+=f'         <div class="move power {stab}">{movepower}</div>'
                                acc = '-' if not move['acc'] else int(move['acc'])
                                htmltext+=f'         <div class="move accuracy">{acc}</div>'
                                contact = ('Y' if move['contact'] else 'N')
                                htmltext+=f'         <div class="move contact">{contact}</div></div>\r\n\t'
                            htmltext+='</div>\r\n' ## Close moves div
                            htmltext+='</div>' ## Close bottom block
                            htmltext+='</div>' ## Close pokemon div
                    htmltext+='</div></div><button id="previous-button">&#8249;</button><button id="next-button">&#8250;</button><script src="reload.js"></script></body></html>' ## Draw the next/previous arrows, close party div, body and HTML
                    if htmltext != prevhtmltext:
                        with open(htmlfile, "w",encoding='utf-8') as f:
                            f.write(htmltext)
                        prevhtmltext=htmltext
                    time.sleep(8.5)
            except Exception as e:
                with open('errorlog.txt','a+') as f:
                    errorLog = str(datetime.now())+": "+str(e)+'\n'
                    f.write(errorLog)
                # traceback.print_exc()
                time.sleep(5)
                print(errorLog)
                if "WinError 10054" in str(e):
                    print("To continue using the tracker, please open a ROM.")
                    print("Waiting for a ROM...")
                    time.sleep(15)
                    game,party_address = getGame()
                    
    finally:
        print("")

BLOCK_SIZE = 56
SLOT_OFFSET = 484
SLOT_DATA_SIZE = (8 + (4 * BLOCK_SIZE))
STAT_DATA_OFFSET = 112
STAT_DATA_SIZE = 22

conn = sqlite3.connect("data/gen67.sqlite")
cursor = conn.cursor()


with open('data/item-data.json','r') as f:
    items = json.loads(f.read())

if __name__ == "__main__" :
    run()