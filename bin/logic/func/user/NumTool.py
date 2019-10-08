import random


class NumTool(object):
    def __init__(self):
        self.prelist = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                        '147', '150', '151', '152', '153', '155', '156', '157', '158', '159',
                        '186', '187', '188', '189']

    def gen_phone_num(self, start_mobile=None):
        if start_mobile is not None:
            return start_mobile + ''.join(random.choice('0123456789') for i in range(8))
        return random.choice(self.prelist) + ''.join(random.choice('0123456789') for i in range(8))

    def gen_QQ(self):
        return ''.join(random.choice('0123456789') for i in range(random.randint(6, 12)))


def getInstance():
    return NumTool()
