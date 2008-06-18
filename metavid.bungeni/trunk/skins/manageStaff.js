window.onload = init;

function init()
{
	var sitting_id = document.getElementById("sitting_id").innerHTML;
  	sajax_request_type='GET';
  	sajax_do_call( 'mv_get_available_editors', [sitting_id] , onReadyEditors ); 
  	sajax_do_call( 'mv_get_available_readers', [sitting_id] , onReadyReaders ); 
  	sajax_do_call( 'mv_get_available_reporters', [sitting_id] , onReadyReporters ); 
  	sajax_do_call( 'mv_get_assigned_editors', [sitting_id] , onReadyAssignedEditors ); 
  	sajax_do_call( 'mv_get_assigned_readers', [sitting_id] , onReadyAssignedReaders ); 
  	sajax_do_call( 'mv_get_assigned_reporters', [sitting_id] , onReadyAssignedReporters ); 
}

function onReadyEditors( req ){
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.staff.available_editors.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var editorname = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var editorid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			//editorid_array[i] = editorid; 
  			document.staff.available_editors.options[i] = new Option(editorname,  editorid, false, false);
		}
	}
}

function onReadyAssignedEditors( req ){
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.staff.assigned_editors.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var editorname = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var editorid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			//editorid_array[i] = editorid; 
  			document.staff.assigned_editors.options[i] = new Option(editorname,  editorid, false, false);
		}
	}
}

function editor_onchange(id)
{
	sajax_request_type='GET';
  	sajax_do_call( 'workload_editor', [id] , load_workload_editor ); 
}

function reader_onchange(id)
{
	sajax_request_type='GET';
  	sajax_do_call( 'workload_reader', [id] , load_workload_reader ); 
}

function reporter_onchange(id)
{
	sajax_request_type='GET';
  	sajax_do_call( 'workload_reporter', [id] , load_workload_reporter ); 
}

function load_workload_editor( req )
{
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	document.getElementById("editor_workload").innerHTML = "";
  	if (req.status!=200) {
    	document.editor_workload.innerHTML = "loading...";
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var sittingname = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var sittingid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;

  			document.getElementById("editor_workload").innerHTML =document.getElementById("editor_workload").innerHTML + "<p>"+sittingname;
		}
	}
}

function load_workload_reporter( req )
{
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	document.getElementById("reporter_workload").innerHTML = "";
  	if (req.status!=200) {
    	document.staff.available_editors.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var sittingname = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var sittingid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;

  			document.getElementById("reporter_workload").innerHTML = document.getElementById("reporter_workload").innerHTML + "<p>"+sittingname;
		}
	}
}

function load_workload_reader( req )
{
	var ready=req.readyState;
	var i = 0;
	document.getElementById("reader_workload").innerHTML="";
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.staff.available_editors.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var sittingname = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var sittingid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			document.getElementById("reader_workload").innerHTML = document.getElementById("reader_workload").innerHTML+"<p>"+sittingname;
		}
	}
}

function onReadyReaders( req ){
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.staff.available_readers.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var readername = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var readerid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			//readerid_array[i] = readerid; 
  			document.staff.available_readers.options[i] = new Option(readername,  readerid, false, false);
		}
	}
}

function onReadyAssignedReporters( req ){
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.staff.assigned_reporters.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var reportername = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var reporterid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			//reporterid_array[i] = reporterid; 
  			document.staff.assigned_reporters.options[i] = new Option(reportername,  reporterid, false, false);
		}
	}
	document.staff.assigned_reporters.options[0].selected = true;
}

function onReadyAssignedReaders( req ){
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.staff.assigned_readers.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var readername = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var readerid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			//readerid_array[i] = readerid; 
  			document.staff.assigned_readers.options[i] = new Option(readername,  readerid, false, false);
		}
	}
	document.staff.assigned_readers.options[0].selected = true;
}

function onReadyReporters( req ){
	var ready=req.readyState;
	var i = 0;
  	data=req.responseXML.documentElement;
  	if (req.status!=200) {
    	document.staff.available_reporters.options[0] = new Option("loading...",0,true,true);
    	return;
    }else
    {	
		for(i=0;i<data.childNodes.length;i++){
  			var reportername = data.childNodes[i].attributes.getNamedItem('name').nodeValue;
  			var reporterid = data.childNodes[i].attributes.getNamedItem('id').nodeValue;
  			//reporterid_array[i] = reporterid; 
  			document.staff.available_reporters.options[i] = new Option(reportername,  reporterid, false, false);
		}
	}
	document.staff.available_reporters.options[0].selected = true;
}

function add_editor()
{
	var value = document.staff.available_editors.options[document.staff.available_editors.selectedIndex].value;
	var text = document.staff.available_editors.options[document.staff.available_editors.selectedIndex].text;
	var lngth = document.staff.assigned_editors.options.length;
	document.staff.assigned_editors.options[lngth] = new Option(text,value,false,false);
	document.staff.available_editors.options[document.staff.available_editors.selectedIndex] = null;
	
}

function remove_editor()
{
	var value = document.staff.assigned_editors.options[document.staff.assigned_editors.selectedIndex].value;
	var text = document.staff.assigned_editors.options[document.staff.assigned_editors.selectedIndex].text;
	var lngth = document.staff.available_editors.options.length;
	document.staff.available_editors.options[lngth] = new Option(text,value,false,false);
	document.staff.assigned_editors.options[document.staff.assigned_editors.selectedIndex] = null;
	
}

function add_reader()
{
	var value = document.staff.available_readers.options[document.staff.available_readers.selectedIndex].value;
	var text = document.staff.available_readers.options[document.staff.available_readers.selectedIndex].text;
	var lngth = document.staff.assigned_readers.options.length;
	document.staff.assigned_readers.options[lngth] = new Option(text,value,false,false);
	document.staff.available_readers.options[document.staff.available_readers.selectedIndex] = null;
	
}

function remove_reader()
{
	var value = document.staff.assigned_readers.options[document.staff.assigned_readers.selectedIndex].value;
	var text = document.staff.assigned_readers.options[document.staff.assigned_readers.selectedIndex].text;
	var lngth = document.staff.available_readers.options.length;
	document.staff.available_readers.options[lngth] = new Option(text,value,false,false);
	document.staff.assigned_readers.options[document.staff.assigned_readers.selectedIndex] = null;
	
}

function add_reporter()
{
	var value = document.staff.available_reporters.options[document.staff.available_reporters.selectedIndex].value;
	var text = document.staff.available_reporters.options[document.staff.available_reporters.selectedIndex].text;
	var lngth = document.staff.assigned_reporters.options.length;
	document.staff.assigned_reporters.options[lngth] = new Option(text,value,false,false);
	document.staff.available_reporters.options[document.staff.available_reporters.selectedIndex] = null;
	
}

function remove_reporter()
{
	var value = document.staff.assigned_reporters.options[document.staff.assigned_reporters.selectedIndex].value;
	var text = document.staff.assigned_reporters.options[document.staff.assigned_reporters.selectedIndex].text;
	var lngth = document.staff.available_reporters.options.length;
	document.staff.available_reporters.options[lngth] = new Option(text,value,false,false);
	document.staff.assigned_reporters.options[document.staff.assigned_reporters.selectedIndex] = null;
	
}

function save()
{
	var i = 0;
	var xml='';
	xml+='<Data>';
	xml+='<AssignedReporters>';
	while (i < document.staff.assigned_reporters.length)
	{
		var value = document.staff.assigned_reporters.options[i].value;
		i++;
		xml += '<reporter id=\"'+value+'\"></reporter>';
	}	
	xml+='</AssignedReporters>';
	xml+='<AssignedReaders>';
	i=0;
	while (i < document.staff.assigned_readers.length)
	{
		var value = document.staff.assigned_readers.options[i].value;
		i++;
		xml += '<reader id=\"'+value+'\"></reader>';
	}	
	xml+='</AssignedReaders>';
	xml+='<AssignedEditors>';
	i=0;
	while (i < document.staff.assigned_editors.length)
	{
		var value = document.staff.assigned_editors.options[i].value;
		i++;
		xml += '<editor id=\"'+value+'\"></editor>';
	}	
	xml+='</AssignedEditors>';
	xml+='</Data>';
	var post_vars = new Object();
	var args = new Object();
	document.getElementById('debug').innerHTML = xml;
	post_vars['xmldata'] = xml;
	post_vars['sitting_id'] = document.getElementById("sitting_id").innerHTML;
	sajax_request_type='POST';
	mv_sajax_do_call('mv_save_staff',args, onResponse, post_vars);
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
