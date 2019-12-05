

class GCounter(object):
  def __init__(self, i, peers):
    self.i = i # server id
    self.peers = peers
    self.peers.append(i)
    self.xs = { key:0 for key in self.peers}

  def query(self):
    return sum(self.xs.values())

  def add(self, x):
    assert x >= 0
    self.xs[self.i] += x

  def merge(self, c):
    #zipped = zip(self.xs.values(), c.xs.values())
    #self.xs = [max(x, y) for (x, y) in zipped]
    inter = set(self.xs) & set(c.xs)
    for i in inter:
        self.xs[i] = max(self.xs[i], c.xs[i])
