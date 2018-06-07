#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random

Facts = [
"Carbon is unique in that it is known to form up to 10 million\ndifferent compounds.\
 Carbon is important to the existence of life.",
"Francium is the rarest element on earth. There are probably\nno more than a few ounces of\
 it on earth at any given time.",
"The only letter not in the periodic table is the letter J.",
"The country Argentina is named after the element silver (symbol Ag)\nwhich is argentum in Latin.",
"Although there is helium on Earth, it was first discovered by observing the sun.",
"Technetium was the first element to be made artificially.",
"The reason why some elements are at the bottom and aren't attached\nto the rest, is to save\
 space and not let the table be as wide.",
"The periodic table has room for 118 elements.",
"The periodic table is considered a 'cheat sheet' to some people \nsince it has the number of valence\
 electrons on top of each column.",
"The bottom elements are named after famous people (ex: einsteinium.)",
"There's only 2 liquids on the periodic table.",
"Carbon is found in diamonds.",
"Elements are technically invisible.",
"There's about 121,000 results on Google on how to memorize the periodic table.",
"The metals are placed to the right of the periodic table.",
"METALLOID: an element that shares properties with metals and some non-metals.",
"The periodic table has served chemistry students since 1869.",
"With a publisher’s deadline looming, Mendeleyev didn’t have time\nto describe all 63\
 then-known elements. So he turned to a data set of atomic\nweights meticulously gathered\
 by others.",
"Fond of card games, Mendeleyev wrote the weight for each element\non a separate index card and\
 sorted them as in solitaire. Elements with similar properties\nformed a “suit” that he\
 placed in columns ordered by ascending atomic weight.",
"Where Mendeleyev’s table had blank spaces, he correctly predicted\nthe weights and\
 chemical behaviors of some missing elements—gallium,\nscandium, and germanium.",
"When argon was discovered in 1894, it didn’t fit into any of Mendeleyev’s\
\ncolumns, so he denied its existence—as he did for helium, neon, krypton, xenon, and radon.",
"In 1902 Mendeleyev acknowledged he had not anticipated the\nexistence of these overlooked,\
 incredibly unreactive elements —the noble gases—\nwhich now constitute the entire eighth\
 group of the table.",
"Today elements are sorted by their number of protons, or 'atomic number',\nwhich\
 determines an atom’s configuration of oppositely charged electrons and\nhence its\
 chemical properties.",
"Noble gases (far right on the periodic table) have closed shells of electrons,\nwhich is\
 why they are nearly inert.",
"Take a modern periodic table, cut out the complicated middle columns,\
\nand fold it once along the middle of the Group 4 elements.\nThe groups that kiss have\
 complementary electron structures and will combine with each other.",
"The Group 4 elements in the middle bond readily with each other and with themselves.\
\nSilicon + silicon + silicon and infinitum links up into crystalline lattices, used\nto\
 make semiconductors for computers.",
"Carbon atoms bond in long chains, and voilà: sugars.\nThe chemical\
 flexibility of carbon is what makes it the key molecule of life.",
"Mendeleyev wrongly assumed that all elements are unchanging.\nBut radioactive\
 atoms have unstable nuclei, meaning they can move around the chart.\nFor example,\
 uranium (element 92) gradually decays into a whole series of lighter elements,\nending\
 with lead (element 82).",
"Beyond the edge: Atoms with atomic numbers higher than 92 do not exist naturally,\n\
but they can be created by bombarding elements with other elements or pieces of them.",
"Physicist Richard Feynman once predicted that number 137 defines the table’s outer\n\
 limit; adding any more protons would produce an energy that could be quantified\nonly by\
 an imaginary number, rendering element 138 and higher impossible. Maybe.",
"Dmitri Mendeleev, known as the “Father” of the Periodic table was\nknown to be a\
 cranky professor teaching at the University of St. Petersburg.",
"Metals are the most common elements found in the Periodic table.",
"With an atomic weight of 1, Hydrogen is the lightest among all the elements\non the\
 periodic table. That is the reason it is located on the left corner of the table.",
"Ever wondered why it is named the periodic table?\nThat’s because the row on the table\
 are called periods.",
"The heaviest element on the periodic table is Uranium with an atomic weight of 238."
]

def get_fact(fact_list):
    current_fact = ''
    for i in range(len(fact_list)):
        random.shuffle(fact_list)
        current_fact = random.choice(fact_list)
        random.shuffle(fact_list)
    return current_fact


