from players.scripts.DSL import DSL
# from players.scripts.part3 import PlayerPart3
import numpy as np



class Synthesizer():
    def synthesize(self):
        dsl = DSL()
        # part3 = PlayerPart3()

        indent_count = 1
        script = dsl.start
        line1 = script.replace('S', np.random.choice(dsl._grammar['S'],p=[0.9, 0.1]))
        # line1 = line1 + ":"
        # print(line1)
        if line1 in ['']:
            line1 = False
            # print(line1)
            return [[' DSL.isDoubles(a) ']]
        while('S' in line1):
            line1_rep = np.random.choice(dsl._grammar['S'],p=[0.4, 0.6])
            # if line1_rep == dsl._grammar['S'][0]:
            #     line1_rep = ": " + line1_rep
            line1 = line1.replace('S', line1_rep)
            # print(line1)

        # line2 = line1.replace('B', np.random.choice(dsl._grammar['B'], p=[0.5, 0.5]))
        # print(line2)
        line2_list = line1.split(' ')
        # print(line2_list)
        for line2_index in range(len(line2_list)):
            if line2_list[line2_index] == 'B':
                line2_list[line2_index] = np.random.choice(dsl._grammar['B'], p=[0.5, 0.5])
        # print(' '.join(line2_list))
        line2 = ' '.join(line2_list)
        # print(line2)
        line3_list = line2.split(' ')
        # print(line3_list)
        for line3_index in range(len(line3_list)):
            if line3_list[line3_index] == 'B1':
                line3_list[line3_index] = np.random.choice(dsl._grammar['B1'])
        # print(' '.join(line3_list))
        # print(line3_list)
        for i in range(1, len(line3_list)):
            if(line3_list[i] in ['if']):
                line3_list[i] = 'and'

        # print(' '.join(line3_list))
        line3 = ' '.join(line3_list)
        line4_list = line3.split(' ')
        # print(line4_list)

        for i in range(len(line4_list)):
            if(line4_list[i] == "NUMBER"):
                line4_list[i] = np.random.choice(dsl._grammar['NUMBER'])
        # print(' '.join(line4_list))

        for i in range((len(line4_list))):
            if(line4_list[i] == "SMALL_NUMBER"):
                line4_list[i] = np.random.choice(dsl._grammar['SMALL_NUMBER'])

        line4 = ' '.join(line4_list)
        line4 = line4.replace('if','')
        line5_list = line4.split('and')
        # print(line5_list)
        rules_list = []
        for rule in line5_list:
            rules_list.append([rule])
        return rules_list



synth = Synthesizer()
synth.synthesize()