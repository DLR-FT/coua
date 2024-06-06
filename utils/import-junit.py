import morph_kgc
import sys


config = """
    [Junit]
    mappings: mappings/junit.ttl 
    file_path: %s
""" % sys.argv[1]

# load XML file, parse using RML mapping provided in config
g = morph_kgc.materialize(config)

# serialize using RDFLib
out = g.serialize(format="turtle")
print(out)
