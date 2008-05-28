
var x = [];

var editorid_array=[];
//var editorname=[];

var id = new Array(100);
for (i = 0; i < id.length; i++)
	id [i] = new Array(100);
	
var names = new Array(100);
for (i = 0; i < names.length; i++)
	names [i] = new Array(100);
	
var unassigned = [];
var READY_STATE_COMPLETE=4;
var data =false;
var numberofeditors;
var previousValue = -1;
window.onload = init;
                           
function onReadyEditors( req ){
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.test.editor.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
   		//removeWhitespace(data);
    	//var editors = data.getElementsByTagName('Editor');
    	//numberofeditors = editors.length;
		for(i=0;i<data.childNodes.length;i++){
			//var readers = editors[i].childNodes;
			//for(j=0;j<readers.length;j++){
  				//var theText = readers[j].attributes.getNamedItem('id').nodeValue;
   				//y[i][j]=theText;
  			//}
  			//editorsid[i] 
  			var editorname = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var editorid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			editorid_array[i] = editorid; 
  			document.test.editor.options[i] = new Option(editorname,  editorid, false, false);
  			for(j=0;j<data.childNodes[i].childNodes.length;j++){
  				var readername = data.childNodes[i].childNodes[j].attributes.getNamedItem('name').nodeValue;
  				var readerid = data.childNodes[i].childNodes[j].attributes.getNamedItem('id').nodeValue;
  				id[i][j] = readerid;
  				names[i][j] = readername;
  			}
		}
		//document.test.editor.options[0].selected = true;
		//while(id[0][i] != undefined)
		//{
			//document.test.assigned.options[i] = new Option( names[0][i], id[0][i], false, false);
			//i++;
		//}
	}
}

function onReadyUnassignedReaders( req ){
	var ready=req.readyState;
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.test.editor.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var readername = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var readerid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			document.test.unassigned.options[i] = new Option(readername,  readerid, false, false);
		}
	}
}

function removeWhitespace(xml)
{
  var loopIndex;
  for (loopIndex = 0; loopIndex < xml.childNodes.length;
    loopIndex++) {
    var currentNode = xml.childNodes[loopIndex];
    if (currentNode.nodeType == 1) {
      removeWhitespace(currentNode);
    }
    if (((/^\s+$/.test(currentNode.nodeValue))) &&
      (currentNode.nodeType == 3)) {
        xml.removeChild(xml.childNodes[loopIndex--]);
    }
  }
}

function load()
{
	var i = 0;
	value = document.test.editor.selectedIndex;
	
	if (previousValue != -1)
	{
		while(id[previousValue][i] != undefined)
		{
			id [previousValue][i] = undefined;
			names [previousValue][i] = undefined;
			i++;
		}
		
		i=0;
		
		while(document.test.assigned.options[0] != null)
		{	
			id[previousValue][i] = document.test.assigned.options[0].value;
			names[previousValue][i] = document.test.assigned.options[0].text;
			document.test.assigned.options[0]=null;
			i++;
		}
	}	
	
	i=0;
	
	while(id[value][i] != undefined)
	{
		document.test.assigned.options[document.test.assigned.options.length] = new Option( names[value][i], id[value][i], false, false);
		i++;
	}
	
	previousValue=value;
}

function add()
{
	var value = document.test.unassigned.options[document.test.unassigned.selectedIndex].value;
	var text = document.test.unassigned.options[document.test.unassigned.selectedIndex].text;
	var lngth = document.test.assigned.options.length;
	document.test.assigned.options[lngth] = new Option(text,value,false,false);
	document.test.unassigned.options[document.test.unassigned.selectedIndex] = null;
	
}

function remove()
{
	var value = document.test.assigned.options[document.test.assigned.selectedIndex].value;
	var text = document.test.assigned.options[document.test.assigned.selectedIndex].text;
	var lngth = document.test.unassigned.options.length;
	document.test.unassigned.options[lngth] = new Option(text,value,false,false);
	document.test.assigned.options[document.test.assigned.selectedIndex] = null;
	
}

function init()
{
  	sajax_request_type='GET';
  	sajax_do_call( 'mv_get_editors', [] , onReadyEditors ); 
  	sajax_do_call( 'mv_get_unassigned_readers', [] , onReadyUnassignedReaders ); 
}

function save()
{
	var i = 0;
	value = document.test.editor.selectedIndex;
	
	if (value != -1)
	{
		while(id[value][i] != undefined)
		{
			id [value][i] = undefined;
			names [value][i] = undefined;
			i++;
		}
		
		i=0;
		
		while( i < document.test.assigned.options.length)
		{	
			id[value][i] = document.test.assigned.options[0].value;
			names[value][i] = document.test.assigned.options[0].text;
			i++;
		}	
		var xml='<? xml version="1.0" encoding="utf-8" ?>';
		xml+='<!DOCTYPE Data>';
		xml+='<Data>';
		var i=0;
		while ( editorid_array[i] != undefined )
		{
			xml += "<Editor id="+editorid_array[i]+">";
			j=0;
			while (id[i][j] != undefined)
			{
				xml += "<Reader id="+id[i][j]+"></Reader>";
				j++;
			}
			xml += "</Editor>";
			i++;
		}
		xml+='</Data>';
		document.getElementById('response').innerHTML=xml;
		var post_vars = new Object();
		var args = new Object();
		post_vars['xmldata'] = xml; 
		sajax_request_type='POST';
		//sajax_do_call('mv_save_editors',post_vars,onResponse);
		mv_sajax_do_call('mv_save_editors',args, onResponse, post_vars);
	}
	else
	{
		document.getElementById('response').innerHTML="No changes made";
	}
}

function onResponse( req )
{
	var ready=req.readyState;
  	var data=req.responseText;
  	if (req.status!=200) {
    	document.getElementById('response').innerHTML="loading...";
    }else
    {	
    	document.getElementById('response').innerHTML=data;
	}
}
