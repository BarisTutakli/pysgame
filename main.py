from classes.game import bgcolors,Person
from classes.magic import Spell
from classes.inventory import Item
import  random

#aşağıda sınıf örnekleri oluşturduk boyna
#Create black magic
fire=Spell("Fire",25,600,"black")
thunder=Spell("Thunder",25,600,"black")
blizzard=Spell("Blizzard",25,600,"black")
meteor=Spell("Meteor",40,1200,"black")
quake=Spell("Quake",14,140,"black")

#create white magic
cure=Spell("Cure",25,620,"white")
cura=Spell("Cura",32,1500,"white")
curaga=Spell("Curaga",50,6000,"white")

#create some items
potion=Item("Potion","potion","Heals 50 HP",50)
hipotion=Item("Hi-Potion","potion","Heals 100 HP",100)
superpotion=Item("Super Potion","potion","Heals 500 HP",1000)
elixer=Item("Elixer","elixer","Fully restores HP/MP of one party member",9999)
hielixer= Item("MegaElixer","elixer","Fully restores HP/MP ",9999)

grenade= Item("Grenade","attack","Deals 500 damage","500")



player_spells=[fire,thunder,blizzard,meteor,quake,cure,cura]
#itemları ayrı ayr key  ile birlikte daha rahat kullanacağız
enemy_spells=[fire,meteor,cure]
player_items=[{"item": potion,"quantity":15},{"item": hipotion,"quantity":5},{"item": superpotion,"quantity":5},
              {"item": elixer, "quantity": 5},{"item": hielixer,"quantity":5},{"item": grenade,"quantity":5}]


#instantiate people
player1=Person("Valos:",3260,138,300,34,player_spells,player_items)
player2=Person("Nick :",4160,188,311,34,player_spells,player_items)
player3=Person("Robot:",3089,175,288,34,player_spells,player_items)

enemy1=Person("Imp    ",1250,130,560,325,enemy_spells,[])
enemy2=Person("Magus",11200,800,525,25,enemy_spells,[])
enemy3=Person("Imp    ",1250,130,560,325,enemy_spells,[])

players=[player1,player2,player3]
enemies=[enemy1,enemy2,enemy3]
print(bgcolors.FAIL+bgcolors.BOLD+"AN ENEMY ATTACK"+bgcolors.ENDC)
running=True
i=1
while running:
    print("*" * 20)

    print("\n\n")
    print("NAME                  HP                                                   MP")
    for player in players:
        player.get_stats()


    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()
    for player in players:

        player.choose_action()
        choice=input("    Choose action: ")
        index=int(choice)-1

        if(index==0):#saldrı türü seçiyor
            dmg=player.generate_damage()#player hasar alıyor
            enemy=player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)#bu kısımda candan hasaraıı çıkartıyor

            print("You attacked "+enemies[enemy].name.replace(" ","")+"for" ,dmg,"points of damage.")#burda bilgi veriyor

            if enemies[enemy].get_hp()==0:
                print(enemies[enemy].name+" has died.")
                del enemies[enemy]
        elif(index==1):
            player.choose_magic()
            magic_choice=int(input("    Choose a magic: "))-1

            if(magic_choice==-1):#büyü seçiyoruz
                continue

            spell=player.magic[magic_choice]
            magic_dmg=spell.generate_damage()#seçilen büyü ile hasar oluştur

            current_mp=player.get_mp()
            if(spell.cost>current_mp):
                print(bgcolors.FAIL+"\n not enough MP \n"+bgcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if(spell.type=="white"):
                print(player.heal(magic_dmg))
                print(bgcolors.OKBLUE+ "\n"+spell.name +" heals for " ,str(magic_dmg), "Hp. "+bgcolors.ENDC)
            elif(spell.type=="black"):
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bgcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to"+enemies[enemy].name.replace(" ","")+bgcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ","") + " has died.")
                    del enemies[enemy]

        elif(index==2):#item ekliyoruz
            player.choose_item()
            item_choice =int(input("    Choose item: "))-1
            if(item_choice==-1):
                continue
        #liste içindeki sözlüklerin item anahtarı ile çağırıp sonra fonksiyon her çalıştığında adadi 1 azaltıyor
            item=player.items[item_choice]["item"]


            if(player.items[item_choice]["quantity"]==0):
                print(bgcolors.FAIL + "\n" +"None left ...."+bgcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1


            if(item.type=="potion"):
                player.heal(int(item.prop))
                print(bgcolors.OKGREEN+"\n"+item.name+ "heals for",str(item.prop),"HP"+bgcolors.ENDC)


            elif(item.type=="elixer"):
                if item.name=="MegaElixer":
                    for i in players:
                        i.hp = i.maxHp
                        i.mp = i.maxmp
                else:
                    player.hp=player.maxHp
                    player.mp=player.maxmp
                print(bgcolors.OKGREEN+"\n"+item.name+ "full restores HP/MP" +bgcolors.ENDC)
            elif(item.type=="attack"):
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bgcolors.FAIL+"\n"+item.name+ "deals",str(item.prop),"points of damage to"+enemies[enemy].name+bgcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ","") + " has died.")
                    del enemies[enemy]
    #check battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if (enemy.get_hp() == 0):
            defeated_enemies += 1

    for player in players:
        if (player.get_hp() == 0):
            defeated_players += 1
            #eğer oyuncu kazanırsa
    if defeated_enemies == 2:
        print(bgcolors.OKGREEN + "You win" + bgcolors.ENDC)
        running = False
    #eğer düşman kazanırsa
    elif (defeated_players) == 2:
        print(bgcolors.FAIL + "You enemies have defeated you", bgcolors.ENDC)
        running = False
    #düşman saldırı bölümü
    for enemy in enemies:


        enemy_choice=random.randrange(0,2)
        if enemy_choice==0:
            #saldırı seç
            target=random.randrange(0,3)
            enemy_dmg=enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ","")+" attacked "+players[target].name.replace(" ","") ,enemy_dmg)
        elif enemy_choice==1:
            spell,magic_dmg=enemy.choose_enemy_spell()
            enemy_choice.reduce_mp(spell.cost)
            if (spell.type == "white"):
                enemy.heal(magic_dmg)
                print(bgcolors.OKBLUE  + spell.name + " heals "+enemy.name +"for ", str(magic_dmg), "Hp. " + bgcolors.ENDC)
            elif (spell.type == "black"):
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)

                print(
                    bgcolors.OKBLUE + "\n"+enemy.name.replace(" ","")+"'s " + spell.name + " deals " + str(magic_dmg) + " points of damage to" + players[
                        target].name.replace(" ", "") + bgcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[player]
            print("Enemy chose",spell,"damage is",magic_dmg)


    #print("-----------------------------------")
    #print("Enemy Hp",bgcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp())+bgcolors.ENDC+"\n")

    #print("Your Hp:",bgcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp())+bgcolors.ENDC)
    #print("Your MP:",bgcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp())+bgcolors.ENDC)




