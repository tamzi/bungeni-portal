function up(field)
{
	//f= document.getElementById(field);
	if ((document.getElementById(field).selectedIndex) > 0)
	{
		var pos = document.getElementById(field).selectedIndex;
		var value = document.getElementById(field).options[pos-1].value;
		var text = document.getElementById(field).options[pos-1].text;
		document.getElementById(field).options[pos-1].value = document.getElementById(field).options[pos].value;
		document.getElementById(field).options[pos-1].text = document.getElementById(field).options[pos].text;
		document.getElementById(field).options[pos].value = value;
		document.getElementById(field).options[pos].text = text;
		document.getElementById(field).options[pos-1].selected = true;
	}
}

function down(field)
{
	f= document.getElementById(field);
	if ((document.getElementById(field).selectedIndex) < (document.getElementById(field).options.length-1))
	{
		var pos = document.getElementById(field).selectedIndex;
		var value = document.getElementById(field).options[pos+1].value;
		var text = document.getElementById(field).options[pos+1].text;
		document.getElementById(field).options[pos+1].value = document.getElementById(field).options[pos].value;
		document.getElementById(field).options[pos+1].text = document.getElementById(field).options[pos].text;
		document.getElementById(field).options[pos].value = value;
		document.getElementById(field).options[pos].text = text;
		document.getElementById(field).options[pos+1].selected = true;
	}
}

function save()
{
	var response = '';
	var i=0;
	response = '<Data>';
	for (i=0; i<document.staff.reporter.options.length;i++)
	{
		response += '<Reporter id=\"'+document.staff.reporter.options[i].value+'\" rank=\"'+(i+1)+'\"></Reporter>';
	}
	
	for (i=0; i<document.staff.reader.options.length;i++)
	{
		response += '<Reader id=\"'+document.staff.reader.options[i].value+'\" rank=\"'+(i+1)+'\"></Reader>';
	}
	
	for (i=0; i<document.staff.editor.options.length;i++)
	{
		response += '<Editor id=\"'+document.staff.editor.options[i].value+'\" rank=\"'+(i+1)+'\"></Editor>';
	}
	response += '</Data>';
	var post_vars = new Object();
	var args = new Object();
	post_vars['xmldata'] = response;
	//post_vars['xmldata'] = '<data></data>';
	sajax_request_type='POST';
	document.getElementById('debug').innerHTML=response;
	mv_sajax_do_call('mv_save_order',args, onReadyResponse, post_vars);
}
function onReadyResponse(req)
{
	var ready=req.readyState;
  	var data=req.responseText;
  	if (req.status!=200) {
    	document.getElementById('success').innerHTML="loading...";
    }else
    {	
    	document.getElementById('success').innerHTML=data;
	}
}
