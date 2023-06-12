import struct
import time
import os
import subprocess
import json
import threading
import traceback
from datetime import datetime
from traceback import print_stack
from citra import Citra

# trackertempfile=open(r"trackertemp.json","r+")
# trackertemp=json.load(trackertempfile)
# print(trackertemp["game"])
# Change this value to your desired game
# if trackertemp["game"]=="XY":
current_game = 1
# if trackertemp["game"]=="ORAS":
#     current_game = 2
# if trackertemp["game"]=="SM":
#     current_game = 3
# if trackertemp["game"]=="USUM":
#     current_game = 4
# Change this value to False to disable auto-layout sprite file management
manage_sprites = False

# -----------------------------------------------------------------------------
## Change these to dictionaries or use sqlite - this is just dex number anyway right?
species = [
"Egg", "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise",
"Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata",
"Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina",
"Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff",
"Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio",
"Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl",
"Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel",
"Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite",
"Magneton", "Farfetchd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly",
"Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor",
"Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey",
"Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx",
"Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon",
"Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres",
"Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion",
"Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados",
"Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy",
"Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom",
"Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown",
"Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish",
"Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine",
"Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan",
"Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou",
"Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic",
"Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple",
"Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow",
"Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth",
"Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass",
"Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric",
"Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel",
"Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria",
"Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep",
"Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius",
"Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth",
"Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios",
"Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup",
"Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray",
"Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen",
"Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary",
"Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly",
"Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas",
"Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow",
"Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon",
"Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie", "Mesprit",
"Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus",
"Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog",
"Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour",
"Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat",
"Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh",
"Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant",
"Basculin", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty",
"Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark",
"Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite",
"Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent",
"Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross",
"Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet",
"Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet",
"Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion",
"Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Meloetta", "Genesect",
"Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier", "Greninja", "Bunnelby", "Diggersby",
"Fletchling", "Fletchinder", "Talonflame", "Scatterbug", "Spewpa", "Vivillon", "Litleo", "Pyroar", "Flabébé", "Floette", "Florges",
"Skiddo", "Gogoat", "Pancham", "Pangoro", "Furfrou", "Espurr", "Meowstic", "Honedge", "Doublade", "Aegislash", "Spritzee", "Aromatisse",
"Swirlix", "Slurpuff", "Inkay", "Malamar", "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Helioptile",
"Heliolisk", "Tyrunt", "Tyrantrum", "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink", "Goomy", "Sliggoo", "Goodra",
"Klefki", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite", "Avalugg", "Noibat", "Noivern", "Xerneas", "Yveltal",
"Zygarde", "Diancie", "Hoopa", "Volcanion", "Rowlet", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne",
"Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable",
"Oricorio", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc", "Wishiwashi", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider",
"Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee",
"Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type: Null", "Silvally",
"Minior", "Komala", "Turtonator", "Togedemaru", "Mimikyu", "Bruxish", "Drampa", "Dhelmise", "Jangmo-o", "Hakamo-o", "Kommo-o",
"Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Nihilego", "Buzzwole", "Pheromosa",
"Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Necrozma", "Magearna", "Marshadow", "Poipole", "Naganadel", "Stakataka",
"Blacephalon", "Zeraora"]

with open('item-data.json','r') as f:
    items = json.loads(f.read())

with open('nature-data.json','r') as f:
    natures = json.loads(f.read())

with open('move-data.json','r') as f:
    movedata = json.loads(f.read())

with open('mon-data.json','r') as f:
    mondata = json.loads(f.read())

with open('movelearn.json','r') as f:
    movelearndata = json.loads(f.read())

## Change these to dictionaries or use sqlite
moves = ["--", "Pound", "Karate Chop", "Double Slap", "Comet Punch", "Mega Punch", "Pay Day", "Fire Punch", "Ice Punch", "Thunder Punch",
"Scratch", "Vice Grip", "Guillotine", "Razor Wind", "Swords Dance", "Cut", "Gust", "Wing Attack", "Whirlwind", "Fly", "Bind", "Slam",
"Vine Whip", "Stomp", "Double Kick", "Mega Kick", "Jump Kick", "Rolling Kick", "Sand Attack", "Headbutt", "Horn Attack", "Fury Attack",
"Horn Drill", "Tackle", "Body Slam", "Wrap", "Take Down", "Thrash", "Double-Edge", "Tail Whip", "Poison Sting", "Twineedle", "Pin Missile",
"Leer", "Bite", "Growl", "Roar", "Sing", "Supersonic", "Sonic Boom", "Disable", "Acid", "Ember", "Flamethrower", "Mist", "Water Gun",
"Hydro Pump", "Surf", "Ice Beam", "Blizzard", "Psybeam", "Bubble Beam", "Aurora Beam", "Hyper Beam", "Peck", "Drill Peck", "Submission",
"Low Kick", "Counter", "Seismic Toss", "Strength", "Absorb", "Mega Drain", "Leech Seed", "Growth", "Razor Leaf", "Solar Beam", "Poison Powder",
"Stun Spore", "Sleep Powder", "Petal Dance", "String Shot", "Dragon Rage", "Fire Spin", "Thunder Shock", "Thunderbolt", "Thunder Wave",
"Thunder", "Rock Throw", "Earthquake", "Fissure", "Dig", "Toxic", "Confusion", "Psychic", "Hypnosis", "Meditate", "Agility", "Quick Attack",
"Rage", "Teleport", "Night Shade", "Mimic", "Screech", "Double Team", "Recover", "Harden", "Minimize", "Smokescreen", "Confuse Ray", "Withdraw",
"Defense Curl", "Barrier", "Light Screen", "Haze", "Reflect", "Focus Energy", "Bide", "Metronome", "Mirror Move", "Self-Destruct", "Egg Bomb",
"Lick", "Smog", "Sludge", "Bone Club", "Fire Blast", "Waterfall", "Clamp", "Swift", "Skull Bash", "Spike Cannon", "Constrict", "Amnesia",
"Kinesis", "Soft-Boiled", "High Jump Kick", "Glare", "Dream Eater", "Poison Gas", "Barrage", "Leech Life", "Lovely Kiss", "Sky Attack",
"Transform", "Bubble", "Dizzy Punch", "Spore", "Flash", "Psywave", "Splash", "Acid Armor", "Crabhammer", "Explosion", "Fury Swipes", "Bonemerang",
"Rest", "Rock Slide", "Hyper Fang", "Sharpen", "Conversion", "Tri Attack", "Super Fang", "Slash", "Substitute", "Struggle", "Sketch", "Triple Kick",
"Thief", "Spider Web", "Mind Reader", "Nightmare", "Flame Wheel", "Snore", "Curse", "Flail", "Conversion 2", "Aeroblast", "Cotton Spore", "Reversal",
"Spite", "Powder Snow", "Protect", "Mach Punch", "Scary Face", "Feint Attack", "Sweet Kiss", "Belly Drum", "Sludge Bomb", "Mud-Slap", "Octazooka",
"Spikes", "Zap Cannon", "Foresight", "Destiny Bond", "Perish Song", "Icy Wind", "Detect", "Bone Rush", "Lock-On", "Outrage", "Sandstorm",
"Giga Drain", "Endure", "Charm", "Rollout", "False Swipe", "Swagger", "Milk Drink", "Spark", "Fury Cutter", "Steel Wing", "Mean Look", "Attract",
"Sleep Talk", "Heal Bell", "Return", "Present", "Frustration", "Safeguard", "Pain Split", "Sacred Fire", "Magnitude", "Dynamic Punch", "Megahorn",
"Dragon Breath", "Baton Pass", "Encore", "Pursuit", "Rapid Spin", "Sweet Scent", "Iron Tail", "Metal Claw", "Vital Throw", "Morning Sun",
"Synthesis", "Moonlight", "Hidden Power", "Cross Chop", "Twister", "Rain Dance", "Sunny Day", "Crunch", "Mirror Coat", "Psych Up", "Extreme Speed",
"Ancient Power", "Shadow Ball", "Future Sight", "Rock Smash", "Whirlpool", "Beat Up", "Fake Out", "Uproar", "Stockpile", "Spit Up", "Swallow",
"Heat Wave", "Hail", "Torment", "Flatter", "Will-O-Wisp", "Memento", "Facade", "Focus Punch", "Smelling Salts", "Follow Me", "Nature Power",
"Charge", "Taunt", "Helping Hand", "Trick", "Role Play", "Wish", "Assist", "Ingrain", "Superpower", "Magic Coat", "Recycle", "Revenge",
"Brick Break", "Yawn", "Knock Off", "Endeavor", "Eruption", "Skill Swap", "Imprison", "Refresh", "Grudge", "Snatch", "Secret Power", "Dive",
"Arm Thrust", "Camouflage", "Tail Glow", "Luster Purge", "Mist Ball", "Feather Dance", "Teeter Dance", "Blaze Kick", "Mud Sport", "Ice Ball",
"Needle Arm", "Slack Off", "Hyper Voice", "Poison Fang", "Crush Claw", "Blast Burn", "Hydro Cannon", "Meteor Mash", "Astonish", "Weather Ball",
"Aromatherapy", "Fake Tears", "Air Cutter", "Overheat", "Odor Sleuth", "Rock Tomb", "Silver Wind", "Metal Sound", "Grass Whistle", "Tickle",
"Cosmic Power", "Water Spout", "Signal Beam", "Shadow Punch", "Extrasensory", "Sky Uppercut", "Sand Tomb", "Sheer Cold", "Muddy Water", "Bullet Seed",
"Aerial Ace", "Icicle Spear", "Iron Defense", "Block", "Howl", "Dragon Claw", "Frenzy Plant", "Bulk Up", "Bounce", "Mud Shot", "Poison Tail",
"Covet", "Volt Tackle", "Magical Leaf", "Water Sport", "Calm Mind", "Leaf Blade", "Dragon Dance", "Rock Blast", "Shock Wave", "Water Pulse",
"Doom Desire", "Psycho Boost", "Roost", "Gravity", "Miracle Eye", "Wake-Up Slap", "Hammer Arm", "Gyro Ball", "Healing Wish", "Brine", "Natural Gift",
"Feint", "Pluck", "Tailwind", "Acupressure", "Metal Burst", "U-turn", "Close Combat", "Payback", "Assurance", "Embargo", "Fling", "Psycho Shift",
"Trump Card", "Heal Block", "Wring Out", "Power Trick", "Gastro Acid", "Lucky Chant", "Me First", "Copycat", "Power Swap", "Guard Swap", "Punishment",
"Last Resort", "Worry Seed", "Sucker Punch", "Toxic Spikes", "Heart Swap", "Aqua Ring", "Magnet Rise", "Flare Blitz", "Force Palm", "Aura Sphere",
"Rock Polish", "Poison Jab", "Dark Pulse", "Night Slash", "Aqua Tail", "Seed Bomb", "Air Slash", "X-Scissor", "Bug Buzz", "Dragon Pulse", "Dragon Rush",
"Power Gem", "Drain Punch", "Vacuum Wave", "Focus Blast", "Energy Ball", "Brave Bird", "Earth Power", "Switcheroo", "Giga Impact", "Nasty Plot",
"Bullet Punch", "Avalanche", "Ice Shard", "Shadow Claw", "Thunder Fang", "Ice Fang", "Fire Fang", "Shadow Sneak", "Mud Bomb", "Psycho Cut", "Zen Headbutt",
"Mirror Shot", "Flash Cannon", "Rock Climb", "Defog", "Trick Room", "Draco Meteor", "Discharge", "Lava Plume", "Leaf Storm", "Power Whip", "Rock Wrecker",
"Cross Poison", "Gunk Shot", "Iron Head", "Magnet Bomb", "Stone Edge", "Captivate", "Stealth Rock", "Grass Knot", "Chatter", "Judgment", "Bug Bite",
"Charge Beam", "Wood Hammer", "Aqua Jet", "Attack Order", "Defend Order", "Heal Order", "Head Smash", "Double Hit", "Roar of Time", "Spacial Rend",
"Lunar Dance", "Crush Grip", "Magma Storm", "Dark Void", "Seed Flare", "Ominous Wind", "Shadow Force", "Hone Claws", "Wide Guard", "Guard Split",
"Power Split", "Wonder Room", "Psyshock", "Venoshock", "Autotomize", "Rage Powder", "Telekinesis", "Magic Room", "Smack Down", "Storm Throw",
"Flame Burst", "Sludge Wave", "Quiver Dance", "Heavy Slam", "Synchronoise", "Electro Ball", "Soak", "Flame Charge", "Coil", "Low Sweep", "Acid Spray",
"Foul Play", "Simple Beam", "Entrainment", "After You", "Round", "Echoed Voice", "Chip Away", "Clear Smog", "Stored Power", "Quick Guard", "Ally Switch",
"Scald", "Shell Smash", "Heal Pulse", "Hex", "Sky Drop", "Shift Gear", "Circle Throw", "Incinerate", "Quash", "Acrobatics", "Reflect Type", "Retaliate",
"Final Gambit", "Bestow", "Inferno", "Water Pledge", "Fire Pledge", "Grass Pledge", "Volt Switch", "Struggle Bug", "Bulldoze", "Frost Breath",
"Dragon Tail", "Work Up", "Electroweb", "Wild Charge", "Drill Run", "Dual Chop", "Heart Stamp", "Horn Leech", "Sacred Sword", "Razor Shell", "Heat Crash",
"Leaf Tornado", "Steamroller", "Cotton Guard", "Night Daze", "Psystrike", "Tail Slap", "Hurricane", "Head Charge", "Gear Grind", "Searing Shot",
"Techno Blast", "Relic Song", "Secret Sword", "Glaciate", "Bolt Strike", "Blue Flare", "Fiery Dance", "Freeze Shock", "Ice Burn", "Snarl", "Icicle Crash",
"V-create", "Fusion Flare", "Fusion Bolt", "Flying Press", "Mat Block", "Belch", "Rototiller", "Sticky Web", "Fell Stinger", "Phantom Force",
"Trick-or-Treat", "Noble Roar", "Ion Deluge", "Parabolic Charge", "Forest’s Curse", "Petal Blizzard", "Freeze-Dry", "Disarming Voice", "Parting Shot",
"Topsy-Turvy", "Draining Kiss", "Crafty Shield", "Flower Shield", "Grassy Terrain", "Misty Terrain", "Electrify", "Play Rough", "Fairy Wind", "Moonblast",
"Boomburst", "Fairy Lock", "King’s Shield", "Play Nice", "Confide", "Diamond Storm", "Steam Eruption", "Hyperspace Hole", "Water Shuriken", "Mystical Fire",
"Spiky Shield", "Aromatic Mist", "Eerie Impulse", "Venom Drench", "Powder", "Geomancy", "Magnetic Flux", "Happy Hour", "Electric Terrain", "Dazzling Gleam",
"Celebrate", "Hold Hands", "Baby-Doll Eyes", "Nuzzle", "Hold Back", "Infestation", "Power-Up Punch", "Oblivion Wing", "Thousand Arrows", "Thousand Waves",
"Land’s Wrath", "Light of Ruin", "Origin Pulse", "Precipice Blades", "Dragon Ascent", "Hyperspace Fury", "Breakneck Blitz", "Breakneck Blitz",
"All-Out Pummeling", "All-Out Pummeling", "Supersonic Skystrike", "Supersonic Skystrike", "Acid Downpour", "Acid Downpour", "Tectonic Rage", "Tectonic Rage",
"Continental Crush", "Continental Crush", "Savage Spin-Out", "Savage Spin-Out", "Never-Ending Nightmare", "Never-Ending Nightmare", "Corkscrew Crash",
"Corkscrew Crash", "Inferno Overdrive", "Inferno Overdrive", "Hydro Vortex", "Hydro Vortex", "Bloom Doom", "Bloom Doom", "Gigavolt Havoc", "Gigavolt Havoc",
"Shattered Psyche", "Shattered Psyche", "Subzero Slammer", "Subzero Slammer", "Devastating Drake", "Devastating Drake", "Black Hole Eclipse",
"Black Hole Eclipse", "Twinkle Tackle", "Twinkle Tackle", "Catastropika", "Shore Up", "First Impression", "Baneful Bunker", "Spirit Shackle", "Darkest Lariat",
"Sparkling Aria", "Ice Hammer", "Floral Healing", "High Horsepower", "Strength Sap", "Solar Blade", "Leafage", "Spotlight", "Toxic Thread", "Laser Focus",
"Gear Up", "Throat Chop", "Pollen Puff", "Anchor Shot", "Psychic Terrain", "Lunge", "Fire Lash", "Power Trip", "Burn Up", "Speed Swap", "Smart Strike",
"Purify", "Revelation Dance", "Core Enforcer", "Trop Kick", "Instruct", "Beak Blast", "Clanging Scales", "Dragon Hammer", "Brutal Swing", "Aurora Veil",
"Sinister Arrow Raid", "Malicious Moonsault", "Oceanic Operetta", "Guardian of Alola", "Soul-Stealing 7-Star Strike", "Stoked Sparksurfer",
"Pulverizing Pancake", "Extreme Evoboost", "Genesis Supernova", "Shell Trap", "Fleur Cannon", "Psychic Fangs", "Stomping Tantrum", "Shadow Bone", "Accelerock",
"Liquidation", "Prismatic Laser", "Spectral Thief", "Sunsteel Strike", "Moongeist Beam", "Tearful Look", "Zing Zap", "Nature’s Madness", "Multi-Attack",
"10,000,000 Volt Thunderbolt", "Mind Blown", "Plasma Fists", "Photon Geyser", "Light That Burns the Sky", "Searing Sunraze Smash",
"Menacing Moonraze Maelstrom", "Let’s Snuggle Forever", "Splintered Stormshards", "Clangorous Soulblaze"]

abilities = ["—", "Stench", "Drizzle", "Speed Boost", "Battle Armor", "Sturdy", "Damp", "Limber", "Sand Veil", "Static", "Volt Absorb",
"Water Absorb", "Oblivious", "Cloud Nine", "Compound Eyes", "Insomnia", "Color Change", "Immunity", "Flash Fire", "Shield Dust", "Own Tempo",
"Suction Cups", "Intimidate", "Shadow Tag", "Rough Skin", "Wonder Guard", "Levitate", "Effect Spore", "Synchronize", "Clear Body", "Natural Cure",
"Lightning Rod", "Serene Grace", "Swift Swim", "Chlorophyll", "Illuminate", "Trace", "Huge Power", "Poison Point", "Inner Focus", "Magma Armor",
"Water Veil", "Magnet Pull", "Soundproof", "Rain Dish", "Sand Stream", "Pressure", "Thick Fat", "Early Bird", "Flame Body", "Run Away", "Keen Eye",
"Hyper Cutter", "Pickup", "Truant", "Hustle", "Cute Charm", "Plus", "Minus", "Forecast", "Sticky Hold", "Shed Skin", "Guts", "Marvel Scale",
"Liquid Ooze", "Overgrow", "Blaze", "Torrent", "Swarm", "Rock Head", "Drought", "Arena Trap", "Vital Spirit", "White Smoke", "Pure Power",
"Shell Armor", "Air Lock", "Tangled Feet", "Motor Drive", "Rivalry", "Steadfast", "Snow Cloak", "Gluttony", "Anger Point", "Unburden", "Heatproof",
"Simple", "Dry Skin", "Download", "Iron Fist", "Poison Heal", "Adaptability", "Skill Link", "Hydration", "Solar Power", "Quick Feet", "Normalize",
"Sniper", "Magic Guard", "No Guard", "Stall", "Technician", "Leaf Guard", "Klutz", "Mold Breaker", "Super Luck", "Aftermath", "Anticipation",
"Forewarn", "Unaware", "Tinted Lens", "Filter", "Slow Start", "Scrappy", "Storm Drain", "Ice Body", "Solid Rock", "Snow Warning", "Honey Gather",
"Frisk", "Reckless", "Multitype", "Flower Gift", "Bad Dreams", "Pickpocket", "Sheer Force", "Contrary", "Unnerve", "Defiant", "Defeatist",
"Cursed Body", "Healer", "Friend Guard", "Weak Armor", "Heavy Metal", "Light Metal", "Multiscale", "Toxic Boost", "Flare Boost", "Harvest",
"Telepathy", "Moody", "Overcoat", "Poison Touch", "Regenerator", "Big Pecks", "Sand Rush", "Wonder Skin", "Analytic", "Illusion", "Imposter",
"Infiltrator", "Mummy", "Moxie", "Justified", "Rattled", "Magic Bounce", "Sap Sipper", "Prankster", "Sand Force", "Iron Barbs", "Zen Mode",
"Victory Star", "Turboblaze", "Teravolt", "Aroma Veil", "Flower Veil", "Cheek Pouch", "Protean", "Fur Coat", "Magician", "Bulletproof",
"Competitive", "Strong Jaw", "Refrigerate", "Sweet Veil", "Stance Change", "Gale Wings", "Mega Launcher", "Grass Pelt", "Symbiosis", "Tough Claws",
"Pixilate", "Gooey", "Aerilate", "Parental Bond", "Dark Aura", "Fairy Aura", "Aura Break", "Primordial Sea", "Desolate Land", "Delta Stream",
"Stamina", "Wimp Out", "Emergency Exit", "Water Compaction", "Merciless", "Shields Down", "Stakeout", "Water Bubble", "Steelworker", "Berserk",
"Slush Rush", "Long Reach", "Liquid Voice", "Triage", "Galvanize", "Surge Surfer", "Schooling", "Disguise", "Battle Bond", "Power Construct",
"Corrosion", "Comatose", "Queenly Majesty", "Innards Out", "Dancer", "Battery", "Fluffy", "Dazzling", "Soul-Heart", "Tangling Hair", "Receiver",
"Power of Alchemy", "Beast Boost", "RKS System", "Electric Surge", "Psychic Surge", "Misty Surge", "Grassy Surge", "Full Metal Body",
"Shadow Shield", "Prism Armor", "Neuroforce"]

naturelookup = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious",
"Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"]

# -----------------------------------------------------------------------------

BLOCK_SIZE = 56
SLOT_OFFSET = 484
SLOT_DATA_SIZE = (8 + (4 * BLOCK_SIZE))
STAT_DATA_OFFSET = 112
STAT_DATA_SIZE = 22

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
        if 0 != first_byte:
            self.raw_data = decrypt_data(encrypted_data)
        else:
            self.raw_data = ""

    def species_num(self):
        if len(self.raw_data) > 0:
            return struct.unpack("<H", self.raw_data[0x8:0xA])[0] ##### Dex number
        else:
            return 0

    def species(self):
        return species[self.species_num()] ############################ Species name

    def name(self):
        speciesname = self.species()
        if self.mega():
            pokemonname = 'Mega '+speciesname
        else:
            pokemonname = speciesname
        return pokemonname

    def bst(self):
        return mondata[self.name()]['bst']
    
    def types(self):
        return mondata[self.species()]['types']

    def held_item_name(self):
        itemnum = str(struct.unpack("<H", self.raw_data[0xA:0xC])[0])
        nm = items[itemnum]['name'].replace("é","&#233;")
        return nm ##################################################### Held item

    def ability(self):
        ability_num = struct.unpack("B", self.raw_data[0x14:0x15])[0] # Ability
        return abilities[ability_num] ## Ability lookup

    def nature(self):
        nature_num = struct.unpack("B", self.raw_data[0x1C:0x1D])[0] ## Nature
        return naturelookup[nature_num] ## Nature lookup
    
####################################################################### EVs
    def ev_hp(self):
        return struct.unpack("B", self.raw_data[0x1E:0x1F])[0] ######## HP EV
    def ev_attack(self):
        return struct.unpack("B", self.raw_data[0x1F:0x20])[0] ######## Attack EV
    def ev_defense(self):
        return struct.unpack("B", self.raw_data[0x20:0x21])[0] ######## Defense EV
    def ev_speed(self):
        return struct.unpack("B", self.raw_data[0x21:0x22])[0] ######## Speed EV
    def ev_sp_attack(self):
        return struct.unpack("B", self.raw_data[0x22:0x23])[0] ######## Special attack EV
    def ev_sp_defense(self):
        return struct.unpack("B", self.raw_data[0x23:0x24])[0] ######## Special defense EV
    
#######################################################################

####################################################################### Moves
    def move_1(self):
        move_num = struct.unpack("<H", self.raw_data[0x5A:0x5C])[0] ### Move 1
        movename = moves[move_num]
        move = {
            'name':movename,
            'pp':struct.unpack("<B",self.raw_data[0x62:0x63])[0],
            'maxpp':movedata[movename]['pp'],
            'type':movedata[movename]['type'],
            'power':movedata[movename]['power'],
            'acc':movedata[movename]['acc'],
            'contact':movedata[movename]['contact'],
            'category':movedata[movename]['detail']
        }
        return move
    
    def move_2(self):
        move_num = struct.unpack("<H", self.raw_data[0x5C:0x5E])[0] ### Move 2
        movename = moves[move_num]
        move = {
            'name':movename,
            'pp':struct.unpack("<B",self.raw_data[0x63:0x64])[0],
            'maxpp':movedata[movename]['pp'],
            'type':movedata[movename]['type'],
            'power':movedata[movename]['power'],
            'acc':movedata[movename]['acc'],
            'contact':movedata[movename]['contact'],
            'category':movedata[movename]['detail']
        }
        return move
    
    def move_3(self):
        move_num = struct.unpack("<H", self.raw_data[0x5E:0x60])[0] ### Move 3
        movename = moves[move_num]
        move = {
            'name':movename,
            'pp':struct.unpack("<B",self.raw_data[0x64:0x65])[0],
            'maxpp':movedata[movename]['pp'],
            'type':movedata[movename]['type'],
            'power':movedata[movename]['power'],
            'acc':movedata[movename]['acc'],
            'contact':movedata[movename]['contact'],
            'category':movedata[movename]['detail']
        }
        return move
    
    def move_4(self):
        move_num = struct.unpack("<H", self.raw_data[0x60:0x62])[0] ### Move 4
        movename = moves[move_num]
        move = {
            'name':movename,
            'pp':struct.unpack("<B",self.raw_data[0x65:0x66])[0],
            'maxpp':movedata[movename]['pp'],
            'type':movedata[movename]['type'],
            'power':movedata[movename]['power'],
            'acc':movedata[movename]['acc'],
            'contact':movedata[movename]['contact'],
            'category':movedata[movename]['detail']
        }
        return move

#######################################################################

####################################################################### IVs
    def iv32(self):
        return struct.unpack("<I", self.raw_data[0x74:0x78])[0]
    def iv_hp(self):
        return (self.iv32() >> 0) & 0x1F ############################## HP IV
    def iv_attack(self):
        return (self.iv32() >> 5) & 0x1F ############################## Attack IV
    def iv_defense(self):
        return (self.iv32() >> 10) & 0x1F ############################# Defense IV
    def iv_speed(self):
        return (self.iv32() >> 15) & 0x1F ############################# Speed IV
    def iv_sp_attack(self):
        return (self.iv32() >> 20) & 0x1F ############################# Special attack IV
    def iv_sp_defense(self):
        return (self.iv32() >> 25) & 0x1F ############################# Special defense IV
    

############################### TEST THESE

    def alt_form(self):
        return struct.unpack("B",self.raw_data[0x1D:0x1E])[0] ### Fateful encounter, Gender, Alternate form data
    
# Bit 0 - Fateful Encounter Flag
# Bit 1 - Female
# Bit 2 - Genderless
# Bit 3-7 - Alternate Forms

    def fatefulencounter(self):
        fateful = (self.alt_form()) & 1
        return fateful == 1

    def female(self):
        female = (self.alt_form() >> 1) & 1
        gender = 'Female' if female else 'Male'
        return gender

    def genderless(self):
        genderless = (self.alt_form() >> 2) & 1
        return genderless == 1

    def mega(self):
        return ((self.alt_form() >> 3) & 1) == 1

    def alt_flags(self):
        for i in range(3,8):
            yield ((self.alt_form() >> i) & 1) == 1 ## Yield an iterator with all 5 flags

    def statuses(self):
        return struct.unpack("<B",bytes(self.raw_data[0xE8:0xE9]))[0] ### Status

    def burned(self):
        burned = (self.statuses() >> 4) & 1
        return burned == 1
    
    def sleepturns(self):
        return (self.statuses()) % (1 << 3)
        ### 000 not asleep --> 0
        ### 001 asleep, but waking up this round --> 1
        ### 010 asleep, waking up next round --> 2
        ### 011 asleep, waking up in 2 rounds --> 3
        ### 100 asleep, waking up in 3 rounds --> 4
        ### 101 asleep, waking up in 4 rounds --> 5
        ### 110 asleep, waking up in 5 rounds --> 6
        ### 111 asleep, waking up in 6 rounds --> 7

    def asleep(self):
        return self.sleepturns() > 0

    def poisoned(self):
        poisoned = (self.statuses() >> 3) & 1
        return poisoned == 1
    
    def frozen(self):
        frozen = (self.statuses() >> 5) & 1
        return frozen == 1
    
    def paralyzed(self):
        paralyzed = (self.statuses() >> 6) & 1
        return paralyzed == 1
    
    def badlypoisoned(self):
        badlypoisoned = (self.statuses() >> 7) & 1
        return badlypoisoned == 1

    def getStatus(self):
        if self.poisoned():
            return 'Poisoned'
        elif self.asleep():
            return 'Asleep'
        elif self.frozen():
            return 'Frozen'
        elif self.paralyzed():
            return 'Paralyzed'
        elif self.burned():
            return 'Burned'
        elif self.badlypoisoned():
            return 'Badly Poisoned'
        else:
            return ''
        
# Bits 0-2 - Asleep (0-7 rounds)
# Bit 3 - Poisoned
# Bit 4 - Burned
# Bit 5 - Frozen
# Bit 6 - Paralyzed
# Bit 7 - Toxic 

#######################################################################

    def friendship(self):
        return str(struct.unpack("B", self.raw_data[0xCA:0xCB])[0]) ### Friendship
    
    def level_met(self):
        return struct.unpack("<H", self.raw_data[0xDD:0xDF])[0] ####### Level met
    def level(self):
        return str(struct.unpack("B", self.raw_data[0xEC:0xED])[0]) ### Current level
    def cur_hp(self):
        return struct.unpack("<H", self.raw_data[0xF0:0xF2])[0] ####### Current HP
    def stat_hp(self):
        return str(struct.unpack("<H", self.raw_data[0xF2:0xF4])[0]) ## Max HP
    def stat_attack(self):
        return str(struct.unpack("<H", self.raw_data[0xF4:0xF6])[0]) ## Attack stat
    def stat_defense(self):
        return str(struct.unpack("<H", self.raw_data[0xF6:0xF8])[0]) ## Defense stat
    def stat_speed(self):
        return str(struct.unpack("<H", self.raw_data[0xF8:0xFA])[0]) ## Speed stat
    def stat_sp_attack(self):
        return str(struct.unpack("<H", self.raw_data[0xFA:0xFC])[0]) ## Special attack stat
    def stat_sp_defense(self):
        return str(struct.unpack("<H", self.raw_data[0xFC:0xFE])[0]) ## Special defense stat

class Pokemon6(Pokemon):
    def __init__(self, data):
        Pokemon.__init__(self, data)

class Pokemon7(Pokemon):
    def __init__(self, data):
        Pokemon.__init__(self, data)

def get_party_address():
    if 1 == current_game:
        return 0x8CE1CE8
    elif 2 == current_game:
        return 0x8CF727C
    elif 3 == current_game:
        return 0x34195E10
    elif 4 == current_game:
        return 0x33F7FA44
    return 0

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def read_party(c):
    party = []
    party_address = get_party_address()
    
    for i in range(6):
        read_address = party_address + (i * SLOT_OFFSET)
        party_data = c.read_memory(read_address, SLOT_DATA_SIZE)
        stats_data = c.read_memory(read_address + SLOT_DATA_SIZE + STAT_DATA_OFFSET, STAT_DATA_SIZE)
        if party_data and stats_data:
            data = party_data + stats_data
            try:
                if 1 == current_game or 2 == current_game:
                    pokemon = Pokemon6(data)
                elif 3 == current_game or 4 == current_game:
                    pokemon = Pokemon7(data)
                party.append(pokemon)
            except ValueError:
                pass
    return party

def launchHTTP():
    subprocess.run(["python", "-m", "http.server"]) ## Launches a local http server to allow the DOM/Axios requests
    print("Please direct an OBS Browser Source to http://localhost/tracker.html or ./tracker.html")

def run():
    print('running..')
    threading.Thread(target=launchHTTP).start()
    htmlfile='tracker.html'
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
                    party = read_party(c)
                    pk=0
                    #print('read party... performing loop')
                    htmltext+='<div id="party">\r\n'
                    for pkmn in party:
                        if 0 != pkmn.species_num():
                            flags = []
                            for flag in pkmn.alt_flags():
                                flags.append(flag)
                            pk=pk+1
                            megaflag = flags[0]
                            iv_average = (pkmn.iv_hp()+pkmn.iv_attack()+pkmn.iv_defense()+pkmn.iv_sp_attack()+pkmn.iv_sp_defense()+pkmn.iv_speed())/6
                            if iv_average > 29:
                                iv_eval = '******'
                            elif iv_average > 24:
                                iv_eval = '*****'
                            elif iv_average > 19:
                                iv_eval = '****'
                            elif iv_average > 14:
                                iv_eval = '***'
                            elif iv_average > 9:
                                iv_eval = '**'
                            elif iv_average > 4:
                                iv_eval = '*'
                            else:
                                iv_eval = '-'
                            ####
                            learnedcount = 0
                            learnlist = movelearndata[str(pkmn.species_num())]
                            totallearn = 0
                            for learn in learnlist:
                                if int(learn) > 1:
                                    totallearn+=1
                            for learn in learnlist:
                                if not int(learn) <= int(pkmn.level()):
                                    nextmove = learn
                                    break
                                elif int(learn) > 1:
                                    learnedcount+=1
                            # print("IVs:")
                            # print(iv_average)
                            if pk == 1:
                                pkstyle = "active"
                            else:
                                pkstyle = "hidden"
                            if pkmn.mega():
                                spriteurl = pkmn.species().lower()+'-mega'
                            else:
                                spriteurl = pkmn.species().lower()
                            htmltext+='<div class="pokemon '+pkstyle+'">\r\n\t'
                            htmltext+='<div class="pokemon-top-block">\r\n\t'
                            htmltext+='<div class="pokemon-top-left-block">\r\n\t'
                            htmltext+='<div class="sprite">\r\n\t<img src="https://img.pokemondb.net/sprites/x-y/normal/'+spriteurl+'.png" data-src="https://img.pokemondb.net/sprites/x-y/normal/'+spriteurl+'.png" width="80" height="80">\r\n</div>\r\n\t'
                            htmltext+='     <div class="species">\r\n\t\t'
                            htmltext+='         <div class="species-number">#'+str(pkmn.species_num())+'</div>\r\n\t\t'
                            htmltext+='         <div class="species-name">'+pkmn.name().replace("Farfetchd","Farfetch&#x27;d")+'</div>\r\n'
                            htmltext+='     </div>\r\n' ## close species
                            htmltext+='<div class="major-stats">\r\n\t'
                            htmltext+='     <div class="level mstat"><span class="name">Level: </span><span class="value">'+str(pkmn.level())+'</span></div>\r\n\t'
                            htmltext+='     <div class="hp mstat"><span class="name">HP: </span><span class="current-hp">'+str(pkmn.cur_hp())+'</span><span id="divisor">/</span><span id="max-hp">'+str(pkmn.stat_hp())+'</span></div>\r\n'
                            htmltext+='     <div class="status mstat"><span class="name">'+pkmn.getStatus()+'</div>'
                            typestr = '<div class="type">'
                            ##### TYPES, STATS, ABIILITIES, ETC.
                            for type in pkmn.types():
                                typestr+='<img src="images/types/'+type+'.png" height="16" width="18"><span class="type '+type+' name">'+type+'</span>'
                                if len(pkmn.types()) > 1 and pkmn.types().index(type) == 0:
                                    typestr+='<span class="type name divider">/</span>'
                            htmltext+='</div>'
                            htmltext+='     <div class="types mstat">'+typestr+'</div>'
                            htmltext+='</div>\r\n' ## Close major stats div
                            htmltext+='<div class="ability">\r\n\t'
                            htmltext+='     <div class="ability-name">'+str(pkmn.ability())+'</div>\r\n'
                            htmltext+='</div>\r\n' ## close ability div
                            htmltext+='<div class="nature">\r\n\t'
                            htmltext+='     <div class="nature-name">'+str(pkmn.nature())+'</div>\r\n'
                            htmltext+='</div>\r\n'
                            htmltext+='<div class="held-item">\r\n\t'
                            htmltext+='     <div class="held-item-name">'+pkmn.held_item_name()+'</div>\r\n'
                            htmltext+='</div>\r\n'
                            htmltext+='</div>\r\n'
                            htmltext+='<div class="pokemon-top-right-block">'
                            ### STATS ########
                            htmltext+='<div class="stats">\r\n'
                            raised = natures[pkmn.nature()]['+'].strip()
                            lowered = natures[pkmn.nature()]['-'].strip()
                            attackchange,defchange,spatkchange,spdefchange,speedchange = '','','','',''
                            if 'Attack' == raised:
                                attackchange = 'raised'
                            elif 'Attack' == lowered:
                                attackchange = 'lowered'
                            if 'Defense' == raised:
                                defchange = 'raised'
                            elif 'Defense' == lowered:
                                defchange = 'lowered'
                            if 'Sp. Attack' == raised:
                                spatkchange = 'raised'
                            elif 'Sp. Attack' == lowered:
                                spatkchange = 'lowered'
                            if 'Sp. Defense' == raised:
                                spdefchange = 'raised'
                            elif 'Sp. Defense' == lowered:
                                spdefchange = 'lowered'
                            if 'Speed' == raised:
                                speedchange = 'raised'
                            elif 'Speed' == lowered:
                                speedchange = 'lowered'
                            htmltext+='     <div class="iv stat"><span class="name">IVs:</span><span class="value">'+iv_eval+'</span></div>\r\n\t'
                            htmltext+='     <div class="attack stat '+attackchange+'"><span class="name">Atk:</span><span class="value">'+str(pkmn.stat_attack())+'</span></div>\r\n\t'
                            htmltext+='     <div class="def stat '+defchange+'"><span class="name">Def:</span><span class="value">'+str(pkmn.stat_defense())+'</span></div>\r\n\t'
                            htmltext+='     <div class="spatk stat '+spatkchange+'"><span class="name">SpAtk:</span><span class="value">'+str(pkmn.stat_sp_attack())+'</span></div>\r\n\t'
                            htmltext+='     <div class="spdef stat '+spdefchange+'"><span class="name">SpDef:</span><span class="value">'+str(pkmn.stat_sp_defense())+'</span></div>\r\n\t'
                            htmltext+='     <div class="speed stat '+speedchange+'"><span class="name">Speed:</span><span class="value">'+str(pkmn.stat_speed())+'</span></div>\r\n\t'
                            htmltext+='     <div class="bst stat"><span class="name">BST:</span><span class="value">'+str(pkmn.bst())+'</span></div>\r\n\t'
                            htmltext+='</div>' ## Close stats div
                            htmltext+='</div>' ## Close top right block
                            htmltext+='</div>' ## Close top block
                            htmltext+='<div class="pokemon-bottom-block">\r\n\t'
                            ### MOVES ########
                            htmltext+='<div class="moves">\r\n\t'
                            htmltext+='     <div class="move label"><div class="move category label">Moves '+str(learnedcount)+'/'+str(totallearn)+' ('+str(nextmove)+')</div><div class="move name label"></div><div class="move maxpp label">PP</div><div class="move power label">BP</div><div class="move accuracy label">Acc</div><div class="move contact label">C</div></div>\r\n\t'
                            for move in [pkmn.move_1(),pkmn.move_2(),pkmn.move_3(),pkmn.move_4()]:
                                htmltext+='     <div class="move '+move['type']+'">'
                                htmltext+='         <div class="move category"><img src="images/categories/'+move['category']+'.png" height="15" width="22"></div>'
                                htmltext+='         <div class="move name">'+move['name']+'</div>'
                                htmltext+='         <div class="move maxpp">'+str(move['pp'])+'/'+str(move['maxpp'])+'</div>'
                                htmltext+='         <div class="move power">'+str('-' if move['power'] == '0' else move['power'])+'</div>'
                                htmltext+='         <div class="move accuracy">'+move['acc'].replace('%','')+'</div>'
                                htmltext+='         <div class="move contact">'+move['contact'].replace("Co.","Y").replace('NC','N')+'</div></div>\r\n\t'
                            htmltext+='</div>\r\n' ## Close moves div
                            htmltext+='</div>' ## Close bottom block
                            htmltext+='</div>' ## Close pokemon div
                    htmltext+='</div><button id="previous-button">&#8249;</button><button id="next-button">&#8250;</button><script src="reload.js"></script></body></html>' ## Draw the next/previous arrows, close party div, body and HTML
                    with open(htmlfile, "w",encoding='utf-8') as f:
                        f.write(htmltext)
                    time.sleep(5)
            except Exception as e:
                with open('errorlog.txt','a+') as f:
                    errorLog = str(datetime.now())+": "+str(e)+'\n'
                    f.write(errorLog)
                traceback.print_exc()
                time.sleep(5)
                print(errorLog)
                if "WinError 10054" in str(e):
                    print("To continue using the tracker, please open a ROM.")
                    print("Waiting for a ROM...")
                    time.sleep(15)
                    
    finally:
        print("")

if "__main__" == __name__:
    run()
