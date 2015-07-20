# congressionalrecord
## This is a fork from the unitedstates GitHub repo.
## It is a branch being rebuilt more or less from the ground up.
## It would not be possible without years of work from volunteers and Sunlight Foundation staffers who found edge cases, built out complex regular expressions, and iterated repeatedly on this project.

Features:

* Parser is modular and extensible: Easy to add and fix edge cases
* Uses beautifulsoup: Slower, but easier to tweak. (TODO: Rewrite back into lxml later.)
* Leverages modularity to parse directory-level data only once. This should speed it up.
* Leverages metadata from XML files provided by THOMAS.gov
* Produces JSON

Currently it can be pointed at a directory and an HTML file in Congressional Record format within that directory, returning a Python dictionary that is easy to convert into a JSON object.

The roadmap starts here and rebuilds all of the functionality of the unitedstates crparser.

The roadmap ends at a project that can produce all the JSON that an ElasticSearch server would need to power a slightly modified, ES-powered Capitolwords.
