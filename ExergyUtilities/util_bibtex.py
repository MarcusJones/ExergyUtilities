import bibtexparser

full_path = r"C:\Dropbox\00 Literature\Main.bib"
full_path = r"C:\Dropbox\Doktorat\LiteratureReview\Main.bib"

with open(full_path) as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)

for i,entry in enumerate(bib_database.entries):
    
    #for key in entry.keys():
    #    print(key)
    f_entry = "{} {} {} {} {}".format(i, entry.get('ENTRYTYPE'), entry.get('title'), entry.get('author'), entry.get('year'))
    entry = [i, entry.get('ENTRYTYPE'), entry.get('title'), entry.get('author'), entry.get('year')]
    entry = [str(item) for item in entry]
    f_entry = " | ".join(entry)
    f_entry = f_entry.replace("\n"," ")
    
    print(f_entry)
    print()
    #print(entry)
    #break