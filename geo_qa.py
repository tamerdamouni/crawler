import lxml.html
import rdflib
import requests

g = rdflib.Graph()
prefix = "http://en.wikipedia.org"
prefix_for_ontology = "http://example.org/"
first_url = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"

countries_url_dict = dict()
people_url_dict = dict()
visited = set()


def concat_prefix_to_entity_or_property(name):
    return f"{prefix_for_ontology}{name}"


president_of = rdflib.URIRef(concat_prefix_to_entity_or_property("president_of"))
population_of = rdflib.URIRef(concat_prefix_to_entity_or_property("population_of"))
born_in = rdflib.URIRef(concat_prefix_to_entity_or_property("born_in"))
bday = rdflib.URIRef(concat_prefix_to_entity_or_property("bday"))
prime_minister_of = rdflib.URIRef(concat_prefix_to_entity_or_property("prime_minister_of"))
capital_of = rdflib.URIRef(concat_prefix_to_entity_or_property("capital_of"))
area_of = rdflib.URIRef(concat_prefix_to_entity_or_property("area_of"))
government_form_of = rdflib.URIRef(concat_prefix_to_entity_or_property("government_form_of"))
official_language_of = rdflib.URIRef(concat_prefix_to_entity_or_property("official_language_of"))


def replace_space(name):
    return name.replace(" ", "_")


def add_urls(name, url, entity_dict):
    final_url = f"{prefix}{url}"
    if final_url not in visited:
        entity_dict[name] = final_url
        visited.add(final_url)


def initiate_url_dict():
    r = requests.get(first_url)
    doc = lxml.html.fromstring((r.content))
    for t in doc.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody//td[1]/span/a'):
        add_urls(t.text, t.attrib['href'], countries_url_dict)


def ie_countries():
    for country_tuple in countries_url_dict.items():
        url = country_tuple[1]
        Country = rdflib.URIRef(concat_prefix_to_entity_or_property(replace_space(country_tuple[0])))
        r = requests.get(url)
        doc = lxml.html.fromstring((r.content))
        # getting capitals
        t = doc.xpath("/html/body/div[3]/div[3]/div[5]/div[1]/table[contains(@class,'infobox')]//tr[contains(th/text("
                      "),'Capital')]//a/text()")
        if len(t) == 0 or t[0] == "de jure":
            Capital = rdflib.URIRef(concat_prefix_to_entity_or_property("None"))
        else:
            Capital = rdflib.URIRef(concat_prefix_to_entity_or_property(replace_space(t[0])))
        #g.add(Capital, capital_of, Country)

        #getting area
        # t = doc.xpath("/html/body/div[3]/div[3]/div[5]/div[1]/table[contains(@class,'infobox')]//tr[contains(text(), 'Area')]/text()")
        # if len(t)!=0:
        #     print(t[0])
        #Area = rdflib.URIRef(concat_prefix_to_entity_or_property(replace_space(t[0])))
        #g.add(Area, area_of, Country)



initiate_url_dict()
ie_countries()
