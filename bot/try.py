sp = [{"parent":"SQL", "child":"SQLALchemy"}]

relations = []
for relat in sp:
    relations.append(tuple(relat.values()))
    
print(relations)