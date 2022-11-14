import random, math
import sys
import assets
from PyQt5.QtWidgets import QApplication, QMainWindow

def miller_rabin(n):
    if n % 2 == 0:
        return False
    u = n - 1
    k = 0
    while (u % 2 == 0):
        u //= 2
        k+=1
    a = random.randint(2,n-2)
    b = pow(a,u,n)
    if b==1 or b ==n-1:
        return True
    for _ in range (1,k-1):
        b= (b*b) % n
        if b==n-1: return True 
        if b==1: return False
    return False


def generateKeys():
        while True:
            p = random.randint(1*10**21, 1*10**22-1)
            q = random.randint(1*10**21, 1*10**22-1)
            if miller_rabin(p) == True and miller_rabin(q) == True and p != q:
                break
        n = p * q
        Fn = (p - 1)*(q - 1)
        while True:
            e = random.randint(2, Fn-1)
            if math.gcd(e, Fn) == 1:
                break
        d = pow(e, -1, Fn)
        return n, e, d


X = 12
z = 10
block = z * X


from PyQt5.uic import loadUi


class MyApp(QMainWindow):


    def submittedKeys(self):
        keyN = self.keyN.toPlainText()
        keyE = self.keyE.toPlainText()
        keyD = self.keyD.toPlainText()
        if len(keyN) == 0 or len(keyE) == 0 or len(keyD) == 0:
            err = "Zadejte klíče"
            self.error.setText(err)
        else:
            keyN = int(keyN)
            keyE = int(keyE)
            keyD = int(keyD)
            if miller_rabin(keyN) and miller_rabin(keyE) and miller_rabin(keyD) and keyN != 0 and keyE != 0 and keyD != 0:
                self.n = keyN
                self.e = keyE
                self.d = keyD
            else:
                err = "Některé z čísel není prvočíslo"
                self.error.setText(err)


    def generateKeys(self):
        self.n, self.e, self.d = generateKeys()
        self.keyN.setPlainText(str(self.n))
        self.keyE.setPlainText(str(self.e))
        self.keyD.setPlainText(str(self.d))


    def encode(self):
        OT = self.inputZasifrovat.toPlainText()
        if len(OT) == 0:
            err = "Prázdný řetězec"
            self.error.setText(err)
        if not self.n or not self.e or not self.d:
            err = "Potřebuji klíče"
            self.error.setText(err)
        OTblocks = [ord(char) for char in OT]
        BINblocks = [bin(ch)[2:].zfill(X) for ch in OTblocks]
        BIN = "".join(BINblocks)
        BINs = [BIN[i:i + block] for i in range(0, len(BIN), block)]
        INTblocks = [int(ch, 2) for ch in BINs]
        c = [pow(ch, self.e, self.n) for ch in INTblocks]
        c = " ".join([str(ch) for ch in c])
        self.outputZasifrovat.setText(c)


    def decode(self):
        ST = self.inputDesifrovat.toPlainText()
        if len(ST) == 0:
            err = "Prázdný řetězec"
            self.error.setText(err)
        if not self.n or not self.e or not self.d:
            err = "Potřebuji klíče"
            self.error.setText(err)
        INTblocks = [int(ch) for ch in ST.split(" ")]
        m = [pow(c, self.d, self.n) for c in INTblocks]
        BINblocks = [bin(ch)[2:].zfill(block) for ch in m]
        BIN = "".join(BINblocks)
        BINs = [BIN[i:i + X] for i in range(0, len(BIN), X)]
        INTs = [int(ch, 2) for ch in BINs]
        output = [chr(ch) for ch in INTs]
        output = "".join(output)
        self.outputDesifrovat.setText(output)


    def __init__(self):
        super(MyApp, self).__init__()
        window = loadUi("gui.ui", self)

        self.generovatKlice.clicked.connect(self.generateKeys)
        self.potvrditKlice.clicked.connect(self.submittedKeys)
        self.zasifrovat.clicked.connect(self.encode)
        self.desifrovat.clicked.connect(self.decode)

        self.n = self.e = self. d = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(app.exec_())
