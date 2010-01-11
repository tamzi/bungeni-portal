function up()
{
	if ((document.test.reporters.selectedIndex) > 0)
	{
		var pos = document.test.reporters.selectedIndex;
		var value = document.test.reporters.options[pos-1].value;
		var text = document.test.reporters.options[pos-1].text;
		document.test.reporters.options[pos-1].value = document.test.reporters.options[pos].value;
		document.test.reporters.options[pos-1].text = document.test.reporters.options[pos].text;
		document.test.reporters.options[pos].value = value;
		document.test.reporters.options[pos].text = text;
		document.test.reporters.options[pos-1].selected = true;
	}
}

function down()
{
	if ((document.test.reporters.selectedIndex) < (document.test.reporters.options.length-1))
	{
		var pos = document.test.reporters.selectedIndex;
		var value = document.test.reporters.options[pos+1].value;
		var text = document.test.reporters.options[pos+1].text;
		document.test.reporters.options[pos+1].value = document.test.reporters.options[pos].value;
		document.test.reporters.options[pos+1].text = document.test.reporters.options[pos].text;
		document.test.reporters.options[pos].value = value;
		document.test.reporters.options[pos].text = text;
		document.test.reporters.options[pos+1].selected = true;
	}
}

function save()
{
	var response = '';
	var i;
	for (i=0; i<document.test.reporters.options.length;i++)
	{
		response = response + document.test.reporters.options[i].value+' ';
	}
	
	var post_vars = new Object();
	var args = new Object();
	post_vars['data'] = response; 
	sajax_request_type='POST';
	//sajax_do_call('mv_save_editors',post_vars,onResponse);
	mv_sajax_do_call('mv_save_reporters',args, onReadyResponse, post_vars);
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
