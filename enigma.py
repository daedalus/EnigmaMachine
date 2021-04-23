class Rotor:
    def __init__(self,name, encoding, rotorPosition, notchPosition, ringSetting):
        #print(self,name, encoding, rotorPosition, notchPosition, ringSetting)
        self.name = name
        self.forwardWiring = self.decodeWiring(encoding)
        self.backwardWiring = self.inverseWiring(self.forwardWiring)
        self.rotorPosition = rotorPosition
        self.notchPosition = notchPosition
        self.ringSetting = ringSetting

    def isAtNotch(self):
        if self.name in ['VI','VII','VIII']:
            return self.rotorPosition == 12 or self.rotorPosition == 25
        else:
            return self.notchPosition == self.rotorPosition

    def Create(name, rotorPosition, ringSetting):
        #print("Rotor.Create",name, rotorPosition, ringSetting) 
        if name == "I":
            return Rotor("I","EKMFLGDQVZNTOWYHXUSPAIBRCJ", rotorPosition, 16, ringSetting)
        elif name == "II":
            return Rotor("II","AJDKSIRUXBLHWTMCQGZNPYFVOE", rotorPosition, 4, ringSetting)
        elif name == "III":
            return Rotor("III","BDFHJLCPRTXVZNYEIWGAKMUSQO", rotorPosition, 21, ringSetting)
        elif name == "IV":
            return Rotor("IV","ESOVPZJAYQUIRHXLNFTGKDCMWB", rotorPosition, 9, ringSetting)
        elif name == "V":
            return Rotor("V","VZBRGITYUPSDNHLXAWMJQOFECK", rotorPosition, 25, ringSetting)
        elif name == "VI":
            return Rotor("VI","JPGVOUMFYQBENHZRDKASXLICTW", rotorPosition, 0, ringSetting)
        elif name == "VII":
            return Rotor("VII","NZJHGRCXMYSWBOUFAIVLPEKQDT", rotorPosition, 0, ringSetting)
        elif name == "VIII":
            return Rotor("VIII","FKQHTLXOCBJSPDZRAMEWNIUYGV", rotorPosition, 0, ringSetting) 
        else:
            return Rotor("Identity","ABCDEFGHIJKLMNOPQRSTUVWXYZ", rotorPosition, 0, ringSetting)

    def getName(self):
        return self.name

    def getPosition(self):
        return self.rotorPosition

    def decodeWiring(self,encoding):
        wiring = [None] * 26
        for i in range(0,len(encoding)):
            wiring[i] = ord(encoding[i]) - 65
        return wiring;
   
    def inverseWiring(self,forwardWiring):
        wiring = [None] * 26 
        for i in range(0,len(forwardWiring)):
            wiring[forwardWiring[i]] = i
        return wiring;

    def encipher(self,k,pos,ring,mapping):
        shift = pos - ring
        return (mapping[(k+shift+26) % 26] - shift + 26) % 26

    def forward(self,c):
        return self.encipher(c, self.rotorPosition, self.ringSetting, self.forwardWiring)
  
    def backward(self,c):
        return self.encipher(c, self.rotorPosition, self.ringSetting, self.backwardWiring)

    def turnover(self):
        self.rotorPosition = (self.rotorPosition + 1) % 26
       

class Plugboard:
    def __init__(self, connections):
        self.wiring = self.decodePlugboard(connections);
 
    def forward(self,c):
        #print(c)
        return self.wiring[c]
    
    def identityPlugboard(self):
        mapping = [x for x in range(0,26)]
        return mapping    

    def removeChar(self,unpluggedCharacters,c):
        try:
            unpluggedCharacters.remove(c)
        except:
            pass
        return unpluggedCharacters
 
    def getUnpluggedCharacters(self,plugboard):
        unpluggedCharacters = []
        for i in range(0,26):
            unpluggedCharacters.append(i)
        if plugboard == "":
            return unpluggedCharacters
        for i in range(0,len(plugboard),2):
            c1 = ord(plugboard[i]) - 65
            c2 = ord(plugboard[i+1]) - 65
            unpluggedCharacters = self.removeChar(c1)
            unpluggedCharacters = self.removeChar(c2)
        return unpluggedCharacters   

    def decodePlugboard(self, plugboard):
        if plugboard == None or plugboard == "":
           return self.identityPlugboard()
        mapping = self.identityPlugboard()
        if len(plugboard) % 2 != 0:
           return self.identityPlugboard()
        pluggedCharacters = []
        for i in range(0,len(plugboard),2):
            c1 = ord(plugboard[i]) - 65
            c2 = ord(plugboard[i+1]) - 65
            if c1 in pluggedCharacters or c2 in pluggedCharacters:
                return self.identityPlugboard()
            pluggedCharacters.append(c1)
            pluggedCharacters.append(c1)
            mapping[c1] = c2
            mapping[c2] = c1
        #print(mapping)
        return mapping

class Reflector:
  def __init__(self, encoding):
     self.forwardWiring = self.decodeWiring(encoding)
   
  def Create(name):
      if name == "B":
          return Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
      elif name == "C":
          return Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")
      else:
          return Reflector("ZYXWVUTSRQPONMLKJIHGFEDCBA")

  def decodeWiring(self,encoding):
      wiring = [None] * 26
      for i in range(0,len(encoding)):
          wiring[i] = ord(encoding[i]) - 65
      return wiring;
 
  def forward(self,c):
        return self.forwardWiring[c]
 
class Enigma:
    def __init__(self,rotors, reflector, rotorPositions, ringSettings, plugboardConnections):
        self.leftRotor = Rotor.Create(rotors[0],rotorPositions[0], ringSettings[0])
        self.middleRotor = Rotor.Create(rotors[1],rotorPositions[1], ringSettings[1])
        self.rightRotor = Rotor.Create(rotors[1],rotorPositions[2], ringSettings[2])
        self.reflector = Reflector.Create(reflector)
        self.plugboard = Plugboard(plugboardConnections)


    def Enigma_key(key):
        self.__init__(key.rotors, "B", key.indicators, key.rings, key.plugboard) 
 
    def rotate(self):
        if self.middleRotor.isAtNotch(): 
            self.middleRotor.turnover()
            self.leftRotor.turnover()
        elif self.rightRotor.isAtNotch():
            self.middleRotor.turnover()
        self.rightRotor.turnover()

    def encrypt_int(self,char):
        self.rotate()
        #print(char)    
        c = self.plugboard.forward(char)
        c1 = self.rightRotor.forward(c);
        c2 = self.middleRotor.forward(c1);
        c3 = self.leftRotor.forward(c2);

        c4 = self.reflector.forward(c3)

        c5 = self.leftRotor.backward(c4);
        c6 = self.middleRotor.backward(c5);
        c7 = self.rightRotor.backward(c6);

        c7 = self.plugboard.forward(c7);

        return c7

    def encrypt_text(self, plaintext):
        tmp = ''
        for i in range(0,len(plaintext)):
            C = ord(plaintext[i]) - 65
            tmp += chr(self.encrypt_int(C) + 65)
        return tmp


def test():
    CT="OZLUDYAKMGMXVFVARPMJIKVWPMBVWMOIDHYPLAYUWGBZFAFAFUQFZQISLEZMYPVBRDDLAGIHIFUJDFADORQOOMIZPYXDCBPWDSSNUSYZTJEWZPWFBWBMIEQXRFASZLOPPZRJKJSPPSTXKPUWYSKNMZZLHJDXJMMMDFODIHUBVCXMNICNYQBNQODFQLOGPZYXRJMTLMRKQAUQJPADHDZPFIKTQBFXAYMVSZPKXIQLOQCVRPKOBZSXIUBAAJBRSNAFDMLLBVSYXISFXQZKQJRIQHOSHVYJXIFUZRMXWJVWHCCYHCXYGRKMKBPWRDBXXRGABQBZRJDVHFPJZUSEBHWAEOGEUQFZEEBDCWNDHIAQDMHKPRVYHQGRDYQIOEOLUBGBSNXWPZCHLDZQBWBEWOCQDBAFGUVHNGCIKXEIZGIZHPJFCTMNNNAUXEVWTWACHOLOLSLTMDRZJZEVKKSSGUUTHVXXODSKTFGRUEIIXVWQYUIPIDBFPGLBYXZTCOQBCAHJYNSGDYLREYBRAKXGKQKWJEKWGAPTHGOMXJDSQKYHMFGOLXBSKVLGNZOAXGVTGXUIVFTGKPJU"

    print(Enigma(["II","V","III"],'',[7,4,19],[12,2,20],"AFTVKOBLRW").encrypt_text(CT))
    print(Enigma(["II","V","III"],'',[12,2,20],[7,4,19],"AFTVKOBLRW").encrypt_text(CT))
    print(Enigma(["II","V","III"],'B',[7,4,19],[12,2,20],"AFTVKOBLRW").encrypt_text(CT))
    print(Enigma(["II","V","III"],'B',[12,2,20],[7,4,19],"AFTVKOBLRW").encrypt_text(CT))
    print(Enigma(["II","V","III"],'C',[7,4,19],[12,2,20],"AFTVKOBLRW").encrypt_text(CT))
    print(Enigma(["II","V","III"],'C',[12,2,20],[7,4,19],"AFTVKOBLRW").encrypt_text(CT))


def test2():
    print(Enigma(['VII','V','IV',],'B',[10,5,12],[1,2,3],"ADFTWHJOPN").encrypt_text('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    print(Enigma(['VII','V','IV',],'B',[1,2,3],[10,5,12],"ADFTWHJOPN").encrypt_text('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    print(Enigma(['IV','V','VII',],'B',[10,5,12],[1,2,3],"ADFTWHJOPN").encrypt_text('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    print(Enigma(['IV','V','VII',],'B',[1,2,3],[10,5,12],"ADFTWHJOPN").encrypt_text('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))







test2()
