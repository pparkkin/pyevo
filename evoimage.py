
import Image
import numpy
import random
from dna import DNA


class EvoImage:
    population_size = 6
    selection_size = 3

    def __init__(self, target=None, callback=None):
        if target:
            self.target = Image.open(target)

        # this function is called with the closest specimen
        # from the population on each iteration
        self.callback = callback

    def set_target(self, target):
        self.target = Image.open(target)

    def run(self):
        pop = self.generate_random_population()
        ng_size = self.population_size - self.selection_size

        gen = 1

        i = 0
        while True:
            i += 1

            ng = self.generate_from_population(pop)
            pop = self.select_from_population(pop+ng)

            if self.callback:
                rep = self.select_from_population(pop, 1)
                self.callback(rep[0])

    def generate_random_population(self):
        pop = []
        width, height = self.target.size
        env = {'width': width, 'height': height}
        for i in range(self.selection_size):
            pop.append(DNA(environ=env))
        return pop

    def generate_from_population(self, pop):
        ng_size = self.population_size - self.selection_size
        ng = []

        for i in range(ng_size):
            p = random.choice(pop)
            c = p.copy()
            c.mutate()
            ng.append(c)

        return ng

    def select_from_population(self, pop, n=-1):
        if n < 0: n = self.selection_size

        pop.sort(lambda x, y:
                imgcompare(x.get_image(), y.get_image(),
                    self.target))
        return pop[:n]

# Image operations

def img2array(im):
    a = numpy.fromstring(im.tostring(), dtype=numpy.uint8)
    a = numpy.reshape(a, (im.size[1], im.size[0], -1))
    return a


def imgcompare(one, two, target):
    width, height = target.size

    # convert images to arrays
    ona = img2array(one)
    tna = img2array(two)
    tga = img2array(target)

    # calculate differences
    diff = tga-ona
    #diff = diff/255
    od = numpy.average(diff)

    diff = tga-tna
    #diff = numpy.abs(diff)
    td = numpy.average(diff)

    # if one is closer to target, return > 0
    # if two is closer to target, return < 0
    # if equal, return 0
    return cmp(od, td)


if __name__ == '__main__':
    def dna_info(dna):
        dna.print_info()
        print dna._image

    ei = EvoImage('monkey.png', dna_info)

    ei.run()


