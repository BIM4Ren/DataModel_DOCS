#!/usr/bin/python

import sys, getopt, os

WIDOCOCMD = """java -jar widoco-1.4.15-jar-with-dependencies.jar\
    -ontFile '{ONTOPATH}' -outFolder 'public/{DOCPATH}'\
    -rewriteAll -webVowl -includeAnnotationProperties -uniteSections"""

HTMLPAGE = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
     <link rel="stylesheet" href="resources/primer.css" media="screen" />    <link rel="stylesheet" href="resources/rec.css" media="screen" />    <link rel="stylesheet" href="resources/extra.css" media="screen" />    <link rel="stylesheet" href="resources/owl.css" media="screen" />    <title>The BIM4Ren buildings ontology</title>


    <!-- SCHEMA.ORG METADATA -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"TechArticle","url":"http://www.bim4ren.eu/buildings#","image":"http://vowl.visualdataweb.org/webvowl/#iri=http://www.bim4ren.eu/buildings#","name":"The BIM4Ren buildings ontology", "headline":"The buildings ontology is part of the BIM4Ren project. It belongs to the core layer, and is an extension of the BOT ontology (Building Ontology Topology). Additional concepts are the possibility to describe a building enveloppe, and to classify buildings and rooms according to their usage.", "datePublished":"Fri Nov 13 18:55:06 CET 2020", "contributor":[{"@type":"Person","name":"Nathalie Charbel"},{"@type":"Person","name":"Pierre Bourreau"}]}</script>

    <script src="resources/jquery.js"></script>
    <script src="resources/marked.min.js"></script>
        <script>
    function loadHash() {
      jQuery(".markdown").each(function(el){jQuery(this).after(marked(jQuery(this).text())).remove()});
    	var hash = location.hash;
    	if($(hash).offset()!=null){
    	  $('html, body').animate({scrollTop: $(hash).offset().top}, 0);
    }
    	loadTOC();
    }
    function loadTOC(){
    	//process toc dynamically
    	  var t='<h2>Table of contents</h2><ul>';i = 1;j=0;
    	  jQuery(".list").each(function(){
    		if(jQuery(this).is('h2')){
    			if(j>0){
    				t+='</ul>';
    				j=0;
    			}
    			t+= '<li>'+i+'. <a href=#'+ jQuery(this).attr('id')+'>'+ jQuery(this).ignore("span").text()+'</a></li>';
    			i++;
    		}
    		if(jQuery(this).is('h3')){
    			if(j==0){
    				t+='<ul>';
    			}
    			j++;
    			t+= '<li>'+(i-1)+'.'+j+'. '+'<a href=#'+ jQuery(this).attr('id')+'>'+ jQuery(this).ignore("span").text()+'</a></li>';
    		}
    	  });
    	  t+='</ul>';
    	  $("#toc").html(t);
    }
    $(function(){
        loadHash();
    }); $.fn.ignore = function(sel){
            return this.clone().find(sel||">*").remove().end();
     };
       </script>
      </head>

    <body>
    <div class="container">
    <div class="head">
    <div style="float:right">language <a href="index-en.html"><b>en</b></a> </div>
    <h1>The BIM4Ren ontology</h1>


    <dl>
    <dt>This version:</dt>
    <dd><a href="http://www.bim4ren.eu/0.1">http://www.bim4ren.eu/0.1</a></dd>
    <dt>Contributors:</dt>
    <dd>Pierre Bourreau</dd><dd>Nathalie Charbel</dd>

    </dl>

    </div>
    <div class="status">
    <div>
    <span>Ontology Specification Draft</span>
    </div>
    </div>     <div id="abstract"><h2>Abstract</h2><span class="markdown">
    The BIM4Ren ontology is a set of ontologies that can be used to model energy efficient renovations. It is built as fully modular ontology and based on
    many current standards or existing ontologies. Close to the IFC schema architecture, it is made of different layers:
    <ul>
    <li> the Core layer: where relation between elements can be specified, in particular to describe the location of the different elements within the building or their role in a MEP network.</li>
    <li> the Product layer: where different classes of products are exposed</li>
    <li> the Domain layer: where properties from different domain (thermal, electrical, acoustic...) can be attached to products</li>
    <li> the Utils layer: where concepts that can be used at different layers are exposed, or useful ontologies that are not specific to the AEC domain.</li>
    It belongs to the core layer, and is an extension of the BOT ontology (Building Ontology Topology). Additional concepts are the possibility to describe a building enveloppe, and to classify buildings and rooms according to their usage.</span>
    </div>
    <p>
    <img src="./Overview.png" alt="Schema of the BIM4Ren ontology" class="center">
    </p>
    <div id="toc"></div>


    <!--OVERVIEW SECTION-->
        <div id="overview"><h2 id="overv" class="list">The BIM4Ren buildings ontology: Overview <span class="backlink"> back to <a href="#toc">ToC</a></span></h2>
    <span class="markdown">
    The BIM4Ren ontology is made of the following ontologies:</span>
    __LISTONTOS__
    </div>
"""

HTMLFOLDER = """<h4>{LAYER}</h4>
<ul class="hlist">
{LISTONTOS}
</ul>"""
HTMLONTO = """<li>
<a href="public/{PATH}/index-en.html" title="{NAME}">
   <span>{NAME}</span>
</a>
</li>"""

def main(argv):
    ontofolder = ''
    docfolder = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'generate-doc.py -i <onto-folder> -o <doc-folder>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generate-doc.py -i <onto-folder> -o <doc-folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            ontofolder = arg
        elif opt in ("-o", "--ofile"):
            docfolder = arg
    ontologies = {}
    ## get all files in the ontology folder
    for root, _, files in os.walk(ontofolder, topdown=True):
        for fname in files:
            if fname.endswith(".ttl"):
                folder = root.lstrip(ontofolder)
                #print(os.path.basename())
                outputfolder, _ = os.path.splitext(os.path.join(folder, fname))
                cmd = WIDOCOCMD.format(
                    ONTOPATH=os.path.join(root, fname),
                    DOCPATH=outputfolder)
                os.system(cmd)
                if (not folder in ontologies):
                    ontologies[folder] = []
                ontologies[folder].append(outputfolder)
    ## generate proper HTML
    strfolder = ""
    for folder in ontologies:
        strontos = ""
        for ontopath in ontologies[folder]:
            ontoname = os.path.basename(ontopath)
            strontos += HTMLONTO.format(PATH=ontopath, NAME=ontoname)
        strfolder += HTMLFOLDER.format(LAYER=folder,
                                       LISTONTOS=strontos)
    content = HTMLPAGE.replace("__LISTONTOS__", strfolder)
    f = open("index.html", "w")
    f.write(content)
    f.close()



if __name__ == "__main__":
    main(sys.argv[1:])
