var linkDLib = 'http://www.dlib.org/dlib/november14/11contents.html';
var documents = 'http://ltw1514.web.cs.unibo.it/project/documents/';
var idClicked;
var documentSelected = false;
var notes = {};
var mode = false;
var count = 0; // variabile per il conteggio delle annotazioni create dall'utente
var time = new Date();
var username;
var email;
var typeOfAnnotation = ["hasAuthor", "hasPublicationYear", "hasTitle", "hasDOI", "hasURL", "hasComment", "denotesRhetoric", "cites"];
var countAnn = 0;
var linkDoc; // variabile per tenere traccia dell'url relativo dell'articolo selezionato
var urlLink; // variabile che tiene traccia dell'url assoluto dell' articolo


/* Funzione che trova tutti i link ai file dei documenti partendo dalla 
 * directory documents e li appende in una lista nella pagine index.html;
 */
function caricaTuttiDocumenti() {

    notes.data = []

    var jsonLinkDLib = JSON.stringify(linkDLib);

    // Chiamata AJAX allo script che esegue web scraping sui link dei documenti e in caso di success carica tutti i link

    $.ajax({
        method: 'POST',
        url: "../cgi-bin/linkDocumentScraping.py",
        cache: false,
        contentType: 'application/json',
        dataType: "json",
        success: function (d) {
            var vet = $.map(d, function (el) {
                return el;
            });
            //console.log(vet);

            for (var x = 0; x < vet.length; x++) {

                // prelevo da href il link
                var link = $(vet[x]).attr('href');

                // tolgo dal link dell'articolo la stringa './' che e' contenuta in alcuni link 
                if (link.indexOf("./") > -1) {
                    var int = link.indexOf("./");
                    link = link.substring(int + 2, link.length);
                }
                var titolo = $(vet[x]).text();
                var linkAnnotation = link.substring(0, link.length - 5); // tolgo dal titolo dell'articolo la parte '.html'
                var annot = linkAnnotation + ".json" // var che serve per salvare in documenti differenti le annotazioni
                    // controllo se i link che trovo hanno una sottostringa 'html'
                if (link.indexOf("november14") > -1) {
                    $('#panelOne').append("<a href='#' onclick='caricoDoc(\"" + link + "\", \"panelUno\")' title=\"" + titolo + "\">" + cleanString(titolo) + "</a><br><hr>");
                } else if (link.indexOf("january13") > -1) {
                    $('#panelTwo').append("<a href='#' onclick='caricoDoc(\"" + link + "\", \"panelDue\")' title=\"" + titolo + "\">" + cleanString(titolo) + "</a><br><hr>");
                } else if (link.indexOf("rivista-statistica") > -1) {
                    $('#panelThree').append("<a href='#' onclick='caricoDoc(\"" + link + "\", \"panelTre\")' title=\"" + titolo + "\">" + cleanString(titolo) + "</a><br><hr>");
                } else if (link.indexOf("almatourism") > -1) {
                    $('#panelFour').append("<a href='#' onclick='caricoDoc(\"" + link + "\", \"panelQuattro\")' title=\"" + titolo + "\">" + cleanString(titolo) + "</a><br><hr>");
                } else if (link.indexOf("encp") > -1) {
                    $('#panelFive').append("<a href='#' onclick='caricoDoc(\"" + link + "\", \"panelCinque\")' title=\"" + titolo + "\">" + cleanString(titolo) + "</a><br><hr>");
                }
            }
        },
        error: function (a, b, c) {
            console.log(a, b, c);
            alert('Error : caricamento lista documenti non riuscito');
        }
    });
}

/* Funzione che chiama  lo script python che fa scraping
 * del wiki salvando i nomi dei gruppi in file json
 * per poi riprenderli e mostrarli nella pagina html
 */
function groupsScraping() {
    // richiama funzione python che fa scraping del wiki per recuperare i gruppi
    $.ajax({
        url: "../cgi-bin/GroupsScraping.py",
        method: "POST",
        success: function (d) {
            //prendo i nomi dei gruppi di tec web e  li appende in un form 
            var obj = $.parseJSON(d)
            for (var x = 0; x < obj.length; x++) {
                $('#groups').append("<span class=\"radio\"><label><input type=\"radio\" value=\"" + obj[x].id + "\" onchange = \"buttonGroupView()\" name=\"optradio\" >" + obj[x].name + "</label></span>");
            }
        },
        error: function (a, b, c) {
            alert('Non ho fatto groups scraping')
            console.log(a, b, c)
        }
    });
}

/*
   Resetta lo stato dei radio input dei gruppi a tutto vuoto
*/

function cleanGroupSelected() {
	var allRadios = document.getElementsByName('optradio');
	for (var i = 0; i< allRadios.length; i++){
		$("input:radio").removeAttr("checked");	}
	buttonGroupHide();
}



/*
   Gestisce la visualizzazione dei pulsanti per la scelta dei gruppi
*/

function buttonGroupView () {
	if ($('#groupRequest').hasClass('hidden')){
        $('#groupRequest').removeClass("hidden");
        $('#cleanGroupRequest').removeClass("hidden");
	} 
}
	
function buttonGroupHide (){
	if (!$('#groupRequest').hasClass('hidden')){
        $('#groupRequest').addClass("hidden");
        $('#cleanGroupRequest').addClass("hidden");
	}
		
}

/*
   Prepara la stringa del testo link in maniera che sia ben visualizzabile
   @param string: stringa nella quale eliminare gli _
   @return: stringa di testo con spazi
*/

function cleanString(string) {
        return string.replace(/_/g, ' ');
    }
    /* Converte il json in un array di stringhe
     * 
     * Parametro iniziale:
     * 
     * - json: file json 
    	  
     */

function stripJsonToString(json) {
    return JSON.stringify(json).replace(',', ', ').replace('[', '').replace(']', '');
}

/* Funzione che carica l'articolo selezionato
 *
 * Paramentri in ingresso:
 * - link: link dell'articolo
 * - id: id del pannello
 */
function caricoDoc(link , id ) {
    var w = 'document';
    //var id = 1;
    var jsonLink = JSON.stringify(link)
    var num = 0
    var l = "";
	var linkWebScrap = []
	
	urlLink = link;
	  
	   switch (id) {
	   case "panelUno":
		   l = "http://www.dlib.org/dlib/november14/";
		   linkWebScrap[0] = "http://www.dlib.org";
		   linkWebScrap[1] = link.substring(linkWebScrap[0].length);
		   break;
	   case "panelDue":
		   l = "http://www.dlib.org/dlib/january13/"
		   linkWebScrap[0] = "http://www.dlib.org";
		   linkWebScrap[1] = link.substring(linkWebScrap[0].length);
		   break;
	   case "panelTre":
		   l = "http://rivista-statistica.unibo.it/article/view/"
		   linkWebScrap[0] = "http://rivista-statistica.unibo.it";
		   linkWebScrap[1] = link.substring(linkWebScrap[0].length);
		   break;
	   case "panelQuattro":
		   l = "http://almatourism.unibo.it/article/view/"
		   linkWebScrap[0] = "http://almatourism.unibo.it";
		   linkWebScrap[1] = link.substring(linkWebScrap[0].length);
		   break;
		   // da cambiare
	   case "panelCinque":
		   l = "http://antropologiaeteatro.unibo.it/article/view/"
		   linkWebScrap[0] = "http://antropologiaeteatro.unibo.it";
		   linkWebScrap[1] = link.substring(linkWebScrap[0].length);
		   break;
	   }
	   var bo = link.substring(l.length) // link relativo all'articolo

       
    $.ajax({
        method: 'POST',
        url: "../cgi-bin/HTMLbodyscraping.py",
        data: jsonLink,
        cache: false,
        contentType: 'application/json',
        dataType: "json",
        success: function (d) {
            linkDoc = bo;
            $('#docum').html('');
            //$('#docum').append('<div id="' + w + id + '"></div>');
            $('#docum').html(d);
            // do un id diverso per ogni elemento del documento
            // rimuovo eventuali attributy style e figli style
            $("#docum").find("*").removeAttr("style");


            $.each($("#docum p"), function (index, value) {
                value.setAttribute('id', "p" + index)
            });
            $.each($("#docum h3"), function (index, value) {
                value.setAttribute('id', "h3" + index)
            });
            $.each($("#docum table"), function (index, value) {
                value.setAttribute('id', "table" + index)
            });
            $.each($("#docum tbody"), function (index, value) {
                value.setAttribute('id', "tbody" + index)
            });
            $.each($("#docum tr"), function (index, value) {
                value.setAttribute('id', "tr" + index)
            });
            $.each($("#docum td"), function (index, value) {
                value.setAttribute('id', "td" + index)
            });
            $.each($("#docum div"), function (index, value) {
                value.setAttribute('id', "div" + index)
            });


        },
        error: function (a, b, c) {
            alert('Errore nel caricamento del documento ' + jsonLink);
            console.debug('error', b + ", " + c + ":\n" + a.responseText);
        }
    });

	$.ajax({
		url: "../cgi-bin/readTriples.py",
		method: "POST",
		cache: false,
		contentType: 'application/json',
		//data: jsonLink,	
		dataType: 'html',
		success: function(data){
				console.log(data);
				//console.log($.parseJSON(data.substr(data.indexOf('{'))))
		},
		error: function(a, b, c) {
            console.log(a.responseText)
            console.log(b)
            console.log(c)
        }
		
	});

    // richiama funzione python che fa web scraping sul documento
    $.ajax({
        url: "../cgi-bin/webScraping.py",
        method: "POST",
        data: JSON.stringify(linkWebScrap),
        dataType: "html",
        //contentType: "string",
        success: function (d) {
			console.log(d)
            // prende da file json il web scraping
            /*
			$.getJSON(linkWebScrap, function (data) {
			for (var i=0; i<data.length; i++){
					notes.data.splice(i, 0, data[i]);
					inserisciNota(notes.data[i], 1);
				} 		
			});
			*/
        },
        error: function (a, b, c) {
            //alert('Non ho fatto web scraping')
			console.log(JSON.stringify(linkWebScrap))
            console.log(a.responseText)
            console.log(b)
            console.log(c)
        }
    });

    if (idClicked != null) {
        $("#" + idClicked).removeClass('active');
    }
    documentSelected = true;
    $('#' + id).addClass('collection-item active');
    idClicked = id;


}


/* Funzione che ritorna la parte evidenziata dall'utente
 *
 */
function selection() {
    if (window.getSelection) {
        return window.getSelection();
    } else if (document.getSelection) {
        return document.getSelection();
    } else if (document.selection) {
        return document.selection.createRange().text;
    }
}

/* Funzione che aggiunge una annotazione
 *
 * Parametri in ingresso:
 * - type: tipo di annotazione (id)
 *
 * agg : subj, pred, liter, label,
 */
function addAnnotazione(type, nameWid) { // nameWid ancora non definito
    var s = selection();
    var data = "";
    var src = "";
    var dad = s.anchorNode.parentElement;
    var pos = dad.childNodes.indexOf(s.anchorNode);
    var datiDaSpedire = new Array()
    var jsonDatiDaSpedire;

    if (s.toString().length > 0) {
        pathID = ""
        src = s.toString();
        x = s.anchorNode.parentNode

        // creo il path del frammento fino al div che contiene l'articolo
        while (x != document.getElementById("docum")) {
            if (x == null) {
                return
            }
            str = x.id + "_"
            pathID += str

            x = x.parentNode
        }

        // jsonDatiDaSpedire = JSON.stringify(type);

        // metto su un array i dati da spedire per creare un'annotazione
        datiDaSpedire.push(type);
        datiDaSpedire.push(linkDoc);
        datiDaSpedire.push(pathID);
        datiDaSpedire.push(s.anchorOffset); // start
        datiDaSpedire.push(s.focusOffset); // end
        datiDaSpedire.push(s.toString()); // selezione del nodo
        datiDaSpedire.push(username);
        datiDaSpedire.push(email);
        datiDaSpedire.push(urlLink);

        jsonDatiDaSpedire = JSON.stringify(datiDaSpedire);
        console.log(datiDaSpedire)

        $.ajax({
            method: 'POST',
            url: "../cgi-bin/creaAnnot.py",
            data: jsonDatiDaSpedire,
            cache: false,
            contentType: 'application/json',
            dataType: "text",
            success: function (d) {
                inserisciNota(datiDaSpedire, dad, pos, 2)

            },
            error: function (a, b, c) {

                console.log(a.responseText)
                console.log(b)
                console.log(c)
                console.log(jsonDatiDaSpedire, dad, pos, dad.id)
            }
        });
        /*
              // sia nell'array delle notes
              notes.data.splice(count, 0, n);
              //inserisco l'annotazione sia visibilmente (parte css)
              inserisciNota(n, 2);
              // sia nella lista per poi salvarle
              appendiAnnotazione(n, count)
              count += 1;
              * */
    } else {
        alert("Seleziona qualcosa per creare un'annotazione!")
    }
}

/* Funzione che apre un modale quando viene cliccata un'annotazione,
 * mostra le sue informazioni
 *
 *  Parametri in ingresso:
 *  - count: numero identificativo dell'annotazione
 *  - nameWid: tipo di widget per l'annotazione
 *  - n: annotazione
 *
 */
function openAnnotationModal(n) {

    var widget = "";

    // tolgo tutto quello che c'era prima
    $('#infoAnnot').html('');
    //console.log(n)
    /* da modificare (WIDGET)
        switch (nameWid) {
        case "Instance":
            widget += ("<select><option value=\"ist1\">istanza 1</option><option value=\"ist2\">istanza 2</option></select>"); //non fa
            break;
        case "Date":
            widget += ("<input type=\"date\" name=\"data\" >");
            break;
        case "LongText":
            widget += ("<textarea name=\"longtext\" rows=\"10\" cols=\"30\"></textarea>");
            break;
        case "ShortText":
            widget += ("<input type=\"text\" name=\"shorttext\" >");
            break;
        case "URL":
            widget += ("<input type=\"url\" name=\"url\" >");
            break;
        case "choice":
            widget += ("<select><option value=\"choice1\">choice 1</option><option value=\"choice2\">choice 2</option></select>"); // non fa
            break;
        case "Citation":

            break;
        }
    */

    // appendo nel modale il tipo di annotazione
    $('#infoAnnot').append("<p><b>Tipo annotazione:</b> " + n[0] + "</p>");
    // appendo il body dell'annotazione (subject, predicate, literal)
    $('#infoAnnot').append("<p><b>Link Documento:</b> " + n[1] + "</p>");
    $('#infoAnnot').append("<p><b>ID Documento:</b> " + n[2] + "</p>");
    $('#infoAnnot').append("<p><b>Start:</b> " + n[3] + "</p>");
    $('#infoAnnot').append("<p><b>End:</b> " + n[4] + "</p>");
    $('#infoAnnot').append("<p><b>Label:</b> " + n[5] + "</p>");
    $('#infoAnnot').append("<hr>")
    $('#infoAnnot').append("<p><b>Username:</b> " + n[6] + "</p>");
    $('#infoAnnot').append("<p><b>Mail:</b> " + n[7] + "</p>");

    $('#saveAnnotationButton').click(function () {
        n[0] = $("#selectListAnnotation option:selected").text();

        // BOOOOOOOOOOOOOOOOO
        /*console.log(n.dati.id)
        if (n.dati.id != null) {
            idAnn = n.dati.id
            eliminaAnnot(idAnn);
            console.log(idAnn, n)
            inserisciNota(n, 2);
        }*/
    });

    // modale per la modifica di una annotazione (type, start, end)
    $('#modificaAnnotationButton').click(function () {
        // tolgo tutto quello che c'era prima
        $('#modifAnnot').html('');

        // aggiungo il select
        $('#modifAnnot').append("<div class=\"form-group col-md-12\"><div class = \"col-lg-10\"><select class = \"form-control\" id=\"selectListAnnotation\"></select> <br> ");
        // popolo il select con ogni elemento dell'array contenente i tipi di annotazioni
        $.each(typeOfAnnotation, function (key, value) {
            $('#selectListAnnotation')
                .append($("<option></option>")
                    .attr("value", value)
                    .text(value));
        });
        $('select option:contains("' + n[0] + '")').prop('selected', true);

        $('#modifAnnot').append()

        $('#modificaAnnotModal').modal()
    });
    // apro il modale 
    $('#gestioneAnnotModal').modal();
}

/* Funzione che elimina l'annotazione
 *
 * Parametri in ingresso:
 *  count: numero identificativo dell'annotazione
 *
 */
function eliminaAnnot(count) {

    document.getElementById(count).removeAttribute("class");
    document.getElementById(count).removeEventListener("click", function (event) {
        openAnnotationModal(n);
        event.preventDefault();
    });
    document.getElementById(count).removeAttribute("id")
    $(" #annot" + count + " ").hide();

    console.log(count)
        // elimina l'annotazione nella posizione specificata da count
    notes.data.splice(count, 1);
}

/* Funzione che inserisce, alla nota passata come paramentro, un attributo alla classe  
 * per colorare la selezione
 *
 * Parametri in ingresso:
 * - n:  dati dell'annotazione da inserire
 * - dad: elemento padre dell'annotazione
 * - pos: posizione dell'annotazione (???)
 * - num:	valore che mi dice se e' una annotazione creata o fatta con web scraping
 *
 */
function inserisciNota(n, dad, pos, num) {
    var r = document.createRange()
    var span = document.createElement('span')
    var node = dad.id;

    console.log(node, n, dad, pos)

    r.setStart(dad.childNodes[pos], parseInt(n[3]))
    r.setEnd(dad.childNodes[pos], parseInt(n[4]))

    /*
    // se num = 1 allora sto facendo web scraping
    if (num == 1) {
        r.setStart(node, n[3]);
        r.setEnd(node, dad.children().length + 1);
    }
    // se num = 2 sto facendo un'annotazione manuale
    else if (num == 2) {
        node = node.childNodes[pos];
        r.setStart(node, parseInt(n[3]));
        r.setEnd(node, parseInt(n[4]));
    }
    * */
    span.setAttribute('class', n[0] + " annotazione-" + n[0])
    span.setAttribute('id', n[2])
    span.addEventListener("click", function (event) {
        openAnnotationModal(n);
        event.preventDefault();
    });
    r.surroundContents(span)

    //node = "";
}

/* Funzione che appende un riassunto delle annotazioni in un modale
 *
 * Parametri in ingresso:
 * - nota: annotazione
 * - int: intero per vedere la posizione in lista
 *
 */
function appendiAnnotazione(nota, count) {
    $('#listaAnnotazioni').append("<li class=\"collection-item avatar\" id=\"annot" + count + "\">" +
        "<span class=\"title\">" + nota.annotations[0].type + "</span>" +
        "<p> TEXTcontent: " + nota.target.source + "</p>" +
        "<p>start: " + nota.target.start + " end: " + nota.target.end + "</p>" +
        "<button type=\"button\" class=\"btn btn-default\" onclick='modAnnot(" + count + ")'><span class=\"glyphicon glyphicon-pencil\" aria-hidden=\"true\"></span></button>" +
        "<button type=\"button\" class=\"btn btn-default\" onclick='eliminaAnnot(" + count + ")'><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></button>");
}

/* Funzione che salva le annotazioni in un file json specifico per ogni articolo
 *
 */
function salvaAnnotazioni() {

    var jsonFile = JSON.stringify(notes)

    $.ajax({
        url: "../cgi-bin/saveAnnot.py",
        method: "POST",
        data: jsonFile,
        dataType: "html",
        contentType: "application/json; charset=utf-8",
        success: function (d) {
            alert("Ho salvato le note!")
            notes = {};
            $('#listaAnnotazioni').html('');
        },
        error: function (a, b, c) {
            //alert('Non ho potuto salvare le note')
            console.log(jsonFile)
            console.log(a)
            console.log(b)
            console.log(c)
        }
    });
}

/* Funzione che esegue il logout
 *
 * */
function confirmLogout() {
    if (confirm("Are you sure? If you exit the changes not saved will be removed.")) {
        // Nascondo i pulsanti dell'utente loggato
        $('#linkLogout').addClass("hidden");
        $('#linkManageAnnotation').addClass("hidden");
        $('#linkDocument').addClass("hidden");
        $('#wellListOfFilter').hide("slow")
        $('#linkLogin').prop('disabled', false);
        // Rinomino il pulsante standard
        $('#linkLogin').html("Login");
    }
}

/* Funzione che controlla nel login la validita delle info immesse
 *
 * */
function checkLogin() {
    try {
        //Validità username
        if ($('#username').val().length > 0) {
            username = $('#username').val();
        } else {
            throw "Inserire la password";
        }
        //Validità e-mail
        if ($('#email').val().length > 0) {
            var regexEmail = /\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;
            email = $('#email').val();
            if (regexEmail.test(email)) {
                //    mail = email;
            } else {
                throw "Indirizzo mail non valido!";
            }
        } else {
            throw "Inserire l'indirizzo mail!";
        }
        //Mostro username annotatore autenticato
        $('#linkLogin').html("<u>" + username + "</u>");
        //Passo in modalità annotatore
        mode = true;
        //Attivo pulsanti modalità annotatore
        $('#linkLogout').removeClass("hidden");
        $('#linkManageAnnotation').removeClass("hidden");
        $('#linkDocument').removeClass("hidden");
        $('#wellListOfFilter').show("slow");
        $('#linkLogin').prop('disabled', true);
        $("#modalLogin").modal("hide");
    } catch (err) {
        alert(err);
        $('#email').val() = '';
        $('#username').val() = '';
    }
}

function searchBarListen() {
    $('#searchBar').keypress(function (e) {
        if (e.which == 13) {
            checkExtension($('#searchBar').val());
            // call a method that check if is .html doc, it's not a douplicate, and generate the link string and pass this at caricoDocumento()
        }
    });
}

function checkExtension(linkToLoad) {
    var extension = linkToLoad.substr((linkToLoad.lastIndexOf('.') + 1));
    switch (extension) {
    case 'html':
        break;
    default:
        alert("The document isn't probabilly formatted");
        //alert('Cannot load the document');
    }

    linkToLoad = prepareForLoadLink(linkToLoad);
    caricoDoc(linkToLoad);
};

function prepareForLoadLink(linkToLoad) {
    if (linkToLoad.indexOf("http") == -1) {
        linkToLoad = "http://" + linkToLoad;
    }
    return linkToLoad;
}


NodeList.prototype.indexOf = function (n) {
    var i = -1;
    while (this.item(i) !== n) {
        i++
    };
    return i
}

/* ---------------------------------------------------------------------
 * --------------------------MAIN---------------------------------------
 * ---------------------------------------------------------------------
 */
function main() {
    caricaTuttiDocumenti();
    groupsScraping();
    searchBarListen();

}

$(document).ready(function () {

    // Funzione che salva le annotazioni

    $('#save').click(function () {
        salvaAnnotazioni();
    })

    // funzione pricipale
    main();

});
