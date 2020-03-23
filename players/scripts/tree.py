import numpy as np
from players.scripts.DSL import DSL

class Tree:
    def __init__(self, dsl):
        self.internal = 'B'
        self.prev = self.internal
        self.dsl = dsl
        # Initialize with a random script first.
        self.prev = self.prev.replace('B', np.random.choice(dsl._grammar['B']))
        while 'B1' in self.prev:
            self.prev = self.prev.replace('B1', np.random.choice(dsl._grammar['B1']), 1)

    def change_tree(self):
        dsl = self.dsl
        prob = np.random.rand(1)[0]
        # The following snippet of code randomly executes a 'big' change or a 'small' change.

        prev = self.prev

        if prob < 0.5:
            # First time
            # print("Previous script is -> ", self.prev)
            prev = self.internal.replace('B', np.random.choice(dsl._grammar['B'])) # Either get 'B1' or 'B1 and 'B1'
            while 'B1' in prev:
                prev = prev.replace('B1', np.random.choice(dsl._grammar['B1']), 1)
            self.prev = prev  # This is the new rule.
            # print("prev is ->", self.prev)
            while 'SMALL_NUMBER' in prev:
                prev = prev.replace('SMALL_NUMBER', np.random.choice(dsl._grammar['SMALL_NUMBER']), 1)
            while 'NUMBER' in prev:
                prev = prev.replace('NUMBER', np.random.choice(dsl._grammar['NUMBER']), 1)
            updated_script = list()
            updated_script.append(prev)
            # print("updated_script is -> ", updated_script)
        else:
            new_script = self.prev
            # print("previous script is ->", new_script)
            while 'SMALL_NUMBER' in new_script:
                new_script = new_script.replace('SMALL_NUMBER', np.random.choice(dsl._grammar['SMALL_NUMBER']), 1)
            while 'NUMBER' in new_script:
                new_script = new_script.replace('NUMBER', np.random.choice(dsl._grammar['NUMBER']),1)
            updated_script = list()
            updated_script.append(new_script)
            # print("Newly updated script is -> ", updated_script)

        return list(updated_script)


# The following snippet of code is for testing purposes!
# The tree representation of the rules seem to be working fine

dsl = DSL()
tree = Tree(dsl)
for i in range(3):
    tree.change_tree()