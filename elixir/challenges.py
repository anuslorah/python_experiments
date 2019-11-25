import time
import random

#stats
def stats(hour, experience, satchel):
  print()
  print("Hour: " + str(hour))
  print("Experience: " + str(experience))
  printsatchel = []
  printsatchel = satchel.copy()
  money = printsatchel.count("gold coin")
  length = len(printsatchel)
  if length > 0:
    i=0
    while i < length:
      if printsatchel[i] == "gold coin":
        printsatchel.remove(printsatchel[i])
        length = length -1  
        continue
      i = i+1
    if money > 0:
      moneycount = str(money) + " gold coins"
      printsatchel.append(moneycount)
  else:
    printsatchel.append("empty")
  print("Satchel: ", end="")
  print(*printsatchel, sep = ", ")
  print()
  time.sleep(2)

def checkTime(hour, experience, satchel):
  if hour >= 13:
    life = "dead"
    print()
    print("Oh no, the sun is setting, your twelve hours are up.")
    print("You crumple onto the ground and die as the last rays of sun disappear from the world.")
    time.sleep(2)
    stats(hour, experience, satchel)
    endScore(hour, experience, satchel)
    False
    
#calculate end score
def endScore(hour, experience, satchel):
  from itertools import permutations 

  counts = []
  counts.append(hour)
  counts.append(experience)

  myItemCount = []
  for i in range(len(satchel)):
    myItemCount.append(i)

  #greedy algorithm to calculate value of items in satchel
  def maxSeq(mylist):
    # get all permutations of the list
    perms = list(permutations(mylist))
    #print(perms)
    # mutiply each permutation by iterative sequence starting with 1 (i=1)
    perms2 = []
    for p in perms:
      i=1
      for r in p:
        perms2.append(r*i)
        i=i+1
    # split results into tuples of 5 elements
    perms3=[]
    it = iter(perms2)
    for chunk in zip(it, it, it, it, it):
      perms3.append(chunk)
    #print(perms3)
    # sum the tuples
    sums = list(map(sum, perms3))
    #print(sums)
    # create dictionary of permutations and sums of tuples
    dictionary = dict(zip(sums, perms))    
    # print sorted dictionary
    #for key in sorted(dictionary):
    #  print( "%s: %s" % (key, dictionary[key]))

    # get max key value
    value = min(dictionary, key=dictionary.get)
    #print("Highest value for given list is: " + str(value) + " for permutation ", end="")
    #print(dictionary[value], end="")
    return [dictionary[value], value]
  
  if len(myItemCount)<5:
    myItemCount.extend([0] * (5 - len(myItemCount))) #pad list
    maxSeq(myItemCount)
    #add items and their greedy value to count
    counts.extend(maxSeq(myItemCount)[0])
    counts.append(maxSeq(myItemCount)[1])
  elif len(myItemCount) >= 5 and len(myItemCount) < 7:
    maxSeq(myItemCount)
    #add items and their greedy value to count
    counts.extend(maxSeq(myItemCount)[0])
    counts.append(maxSeq(myItemCount)[1])
  else:
    myItemCount2=[]
    for i in range(7):
      myItemCount2.append(random.choice(myItemCount))
    maxSeq(myItemCount2)
    #add items and their greedy value to count
    counts.extend(maxSeq(myItemCount2)[0])
    counts.append(maxSeq(myItemCount2)[1])  
  
  print(counts)
  score = sum(counts)+1
  
  #put count to binary tree
  class Node():
    def __init__(self, key, data):
      self.key = key #index of the element
      self.data = data
      self.left = None
      self.right = None

  #first recursion
  def bstInsert(root, node):
    if root == None: #empty tree
      root = node
    else:
      if root.key < node.key: 
        if root.right is None: #no right tree
          root.right = node
        else:
          bstInsert(root.right, node)
      else:
        if root.left is None:
          root.left = node
        else:
          bstInsert(root.left, node)

  myRoot = Node(hour, hour)
  for i in range(len(counts)): 
    bstInsert(myRoot, Node(counts[i], counts[i]))

  #if tree is balanced, +10 to sum of count
  #second recursion
  def tree_height(root):
    if root is None: 
      return 0
    else:
      return 1 + max(tree_height(root.left), tree_height(root.right))

  #third recursion
  def check_balance(root):
    #empty tree is balanced
    if root is None: 
      return True
    else:
      return check_balance(root.right) and check_balance(root.left) and abs(tree_height(root.left) - tree_height(root.right)) <= 1

  if check_balance(myRoot):
    score = score + 10

    #find smallest value
  def minValueNode(node):
    current = node
    #go to leftmost leaf
    while current.left is not None:
      current = current.left
    return current
    
  #fourth recursion
  #delete node
  def deleteNode(root, key):
    #base case
    if root is None:
      return root
    #traverse until find the node to be deleted
    #going left
    if key < root.key:
      root.left = deleteNode(root.left, key)
    #going right  
    elif key > root.key:
      root.right = deleteNode(root.right, key)
    #key found, 
    else:
      #node with one child or no children
      if root.left is None:
        temp = root.right
        root =None
        return temp
      elif root.right is None:
        temp = root.left
        root = None
        return temp
      #node with 2 children, smallest in the right subtree
      temp = minValueNode(root.right)
    #copy inorder sucessor to this nore
      root.key = temp.key
    #delete inorder successot
      root.right = deleteNode(root.right, temp.key)
    return root


  #deleteNode(myRoot, 9)
  #print final score
  print("Your final score is " + str(score))
  print()

#sphinx
def sphinx():
  import random
  life = "alive"
  print()
  print("The sphinx opens one large eye and says:")
  time.sleep(1)
  print("I have a riddle, if you can answer it correctly, you can pass.")
  print("If you fail, you die.")
  print()
  r = random.randint(1,7)
  if r == 1:
    print("What starts with T, ends with T and is full of T?")
    print()
    answer = input("Type our answer: ").lower().strip()
    if answer == "teapot":
      time.sleep(2)
      print("You are correct.")
    else:
      time.sleep(2)
      print("Your answer is wrong.")
      life = "dead"
  elif r == 2:
    print("This thing all things devours;\n Birds, beasts, trees, flowers;\nGnaws iron, bites steel;\n Grinds hard stones to meal;\n Slays king, ruins town,\n And beats mountain down.")
    time.sleep(1)
    print("...four letters...")
    time.sleep(2)
    print()
    answer = input("Type our answer: ").lower().strip()
    if answer == "time":
      time.sleep(2)
      print("You got it right. You may pass.")
    else:
      time.sleep(2)
      print("You are so wrong.")
      life = "dead"
  elif r == 3:
    print("If you threw a white stone into the Red Sea, what would it become?")
    time.sleep(1)
    print("...three letters..")
    print()
    answer = input("Type our answer: ").lower().strip()
    if answer == "wet":
      time.sleep(2)
      print("You got this one right.")
    else:
      time.sleep(2)
      print("No, that is not it.")
      life = "dead"
  elif r == 4:
    print("What creature walks on four legs in the morning,/n two at noon, and three in the evening?")
    time.sleep(1)
    print("...three letters..")
    print()
    answer = input("Type our answer: ").lower().strip()
    if answer == "man":
      time.sleep(2)
      print("Have I been asking this one too long? You are correct.")
    else:
      time.sleep(2)
      print("You are wrong.")
      life = "dead"
  elif r == 5:
    print("What time is spelled the same forwards and backwards?")
    time.sleep(1)
    print("...four letters..")
    print()
    answer = input("Type our answer: ").lower().strip()
    if answer == "noon":
      time.sleep(2)
      print("This is correct.")
    else:
      time.sleep(2)
      print("You are not right.")
      life = "dead"
  else:
    print("Mary’s father has five daughters – Nana, Nene, Nini, and Nono./n What is the fifth daughter’s name?")
    time.sleep(1)
    print("...four letters..")
    print()
    answer = input("Type our answer: ").lower().strip()
    if answer == "mary":
      time.sleep(2)
      print("You answer is correct.")
    else:
      time.sleep(2)
      print("You are wrong.")
      life = "dead"
  return life

#primary number game challenge
def primeGame(experience, satchel):
  print("The letters on the wall look like this:")
  print()
  print(" a -  b - c ")
  print("   \     / ")
  print("      d   ")
  print("   /     \ ")
  print(" e -  f  - g ")

  print("The numbers on the rocks are: 5, 7, 11, 13, 17, 19, 23")
  print("To unlock the secret door, place numbers stones on the letters slots so that")
  print("a + b + c = 41")
  print("a + d + g = 41")
  print("e + d + c = 41")
  print("and e + f + g = 41")

  a = int(input("a="))
  b = int(input("b="))
  c = int(input("c="))
  d = int(input("d="))
  e = int(input("e="))
  f = int(input("f="))
  g = int(input("g="))

  if (a+b+c==41 and a+d+g==41 and e+d+c==41 and e+f+g==41):
    print(" 5 - 19 - 17")
    print("   \    / ")
    print("     13  ")
    print("   /    \ ")
    print("11 - 7  - 23")
    print("Door unlocked!!!")
    experience = experience + 15
    
  else:
    print("Nope, that's not it. Try again!")
    print("If you have a book, you could look for a hint..")
    if "book" in satchel:
      print("You look in your satchel and oh the luck!")
      print("You happened to pick up that dog eared book by the river.")
      print("Leafing through the book you come across a smudged page:")
      print(" 5 - ** - 17")
      print("   \    / ")
      print("     **  ")
      print("   /    \ ")
      print("11 - ** - 23")
      print()
      print("Now you only need to place 7, 13 and 19")
      print("Try again:")
      b = int(input("b="))
      d = int(input("d="))
      f = int(input("f="))

      if b==19 and d==13 and f==9:
        print(" 5 - 19 - 17")
        print("   \    / ")
        print("     13  ")
        print("   /    \ ")
        print("11 - 7  - 23")
        print("Door unlocked!!!")
        experience = experience + 15
      else: 
        print("Try again:")
        b = int(input("b="))
        d = int(input("d="))
        f = int(input("f="))


    experience = experience + 1

#convert decimal to binary
def dec2bin(dec):
  #cast to int
  dec = int(dec)
  binary = []
  #edge case
  if dec == 0:
    print(dec, " in binary is ", dec)
  #iterate through numbers and convert ot binary  
  while dec:
    binary.append(dec%2)
    #shift bitwise right and assign value to left operand
    dec >>= 1
  #print(binary)
  #print(binary[::-1])
  #cast to string and join but reversed
  newbinary = ''.join(str(e) for e in binary[::-1])
  return newbinary
#end of dec2bin(dec) 

#binary challenge
def binaryChallenge(experience):
  import random
  
  r = random.randint(1,11)
  print(r)
  print("There are two kinds of people in the world,")
  print("those who understand binary and those who don't.")
  print("This is your chance to prove you belong to the elite group..")
  print("Can you do it?")    
  if input("Convert " + str(r) + " to binary: ") == dec2bin(int(r)):
    print()
    print("You got it! You beat the troll!")
    experience = experience + 10

  else:
    print("Too bad..")
    print("The right answer would have been " + str(dec2bin(int(r))))
    experience = experience + 1


def getInput(prompt):
    value = input(prompt)
    while not value.isnumeric():
        print("This is not a valid choice")
        value = input("Please enter a number ")
    return int(value)

#getInput("moo?")