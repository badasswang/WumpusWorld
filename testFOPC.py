import FOPC

statement1 = ('clean', 'Cell 11')
statement2 = ('calm', 'Cell 11')

statement3 = ('nasty', 'Cell 12')
statement4 = ('calm', 'Cell 12')

statement5 = ('clean', 'Cell 21')
statement6 = ('breeze', 'Cell 21')

pattern_clean = ('clean', '?x')
pattern_nasty = ('nasty', '?x')
pattern_calm = ('calm', '?x') 
pattern_breeze = ('breeze', '?x') 

knowledge_base = {}

#knowledge_base = FOPC.match(statement1,pattern_clean,knowledge_base)
#knowledge_base = FOPC.match(statement2,pattern_calm,knowledge_base)
#third = FOPC.match(statement3,pattern_nasty,bindings2)
#four = FOPC.match(statement4,pattern_calm,bindings2)

# second = FOPC.match(statement2,pattern,first)

test_statement4 = ('breeze', 'Cell 12')

print FOPC.instantiate([statement1,statement2,statement3,statement4,statement5,statement6], knowledge_base)
#FOPC.instantiate(statement2, knowledge_base)
#print FOPC.instantiate(statement3, third)
#print FOPC.instantiate(statement4, four)

print FOPC.match(('clean', 'Cell 12'),('clean', 'Cell 12'),knowledge_base)


