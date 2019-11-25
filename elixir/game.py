from challenges import stats
from random import random

# transitions
def intro():
  print('You wake up in the dim woods. The edge of the sky is getting lighter.')
  print('You hear water burbling in the distance. Next to you is a leather satchel')
  print('and a note: "You have one day to find the elixir of life or die". ')
  print('You look up. The first rays of sunlight have just broken over the horizon.')
  print()

room1 = ('room1', 'The trees are tall as cathedrals. The leaves whisper in the wind.\nYou look around. There is an overgrown path running East to West.')
room2 = ('East, towards the river', 'The sound of water gets louder. Soon you come to a river\nbank. You look up and down the river. There is no bridge in sight.\nYou look behind you: the path you have followed here \nhas disappeared. But there is hope! On the other side of \nthe river is a wide footpath running along the bank.')
room3 = ('room3', 'The sun has disappeared behind the clouds. You start walking towards \nthe south. There is a loud crashing sound behind you. \nYou look back and see that the footpath has been blocked \nby a huge boulder. Nothing to do but to continue onward. \nYou come to a bridge. Of course it is not a regular bridge. \nThere is a troll challenging you.')
room4 = ('West, deeper into the woods', 'You are in room 4')
room5 = ('room5', 'You are in room 5')
room6 = ('room6', 'You are in room 6')
end = ('end', 'You have made it to the end!')

transitions = {
  room1: (room2, room4),
  room2: (room6, room3),
  room3: (room2, room4, room6),
  room4: (room1, room3, room5),
  room5: (room4, room6),
  room6: (room3, room5, end),
  end:(end)
}

#starting location
intro()
hour = 0
experience = 0
satchel = []
probability = 0
location = room1
while True:
  print(location[1])
  if location == room1:
    #what happens
    print()
    print("You see an axe lying on the ground.")
    print("1 pick up the axe and put it in your satchel")
    print("2 do not pick up the axe")
    doWhat = int(input("Do you want to pick it up? "))
    if doWhat ==1:
      satchel.append("axe")
      experience = experience + 2
    else:
      experience = experience + 1
    stats(hour, experience, satchel)
    hour = hour + 2 
  elif location == room2:  
    #what happens
    print("You see a dog-eared book on the ground.")
    print("1 pick up the book and put it in your satchel")
    print("2 do not pick up the book")
    doWhat = int(input("Do you want to pick it up? "))
    if doWhat ==1:
      satchel.append("book")
      experience = experience + 2
    else:
      experience = experience + 1
    stats(hour, experience, satchel)

    print("Right at the edge of the river is a tree. \nIf you have an axe you can cut down the tree and \nuse it as a bridge. Otherwise you have to swim across.")
    print("1 swim across the river")
    print("2 chop down a tree to make a bridge")
    doWhat = int(input("What do you want to do? "))
    if doWhat == 1:
      probability = random()
      #probability = 0.1
      if probability <= 0.25:
        print("You drown..")
        stats(hour, experience, satchel)
        #location = "end"
        False
        break
      else:
        print("You made it across the river.")
      experience = experience + 5
    else:
      if "axe" not in satchel:
        print("You don't have an axe")
      else:
        print("you made a bridge!")
      experience = experience + 10
    hour = hour + 1
  elif location == room3:
    #what happens
    stats(hour, experience, satchel)
  elif location == room4:
    #what happens
    stats(hour, experience, satchel)
  elif location == room5:
    #what happens
    stats(hour, experience, satchel)
  elif location == room6:
    #what happens
    stats(hour, experience, satchel)
  elif location == end:
    #what happens
    stats(hour, experience, satchel)

  print('You can go to these places:')
  for (i, t) in enumerate(transitions[location]):
    print(i+1, t[0])
    print()

  choice = int(input("Choose where you wan to go: "))
  location = transitions[location][choice-1]
  if location == end:
    print('You win!')
    False
    break
    

