<?php

class MV_AjaxResponse extends AjaxResponse
{
	function __construct($text=NULL)
	{
		parent::__construct($text);
	}
	function getText()
	{
		return $this->mText;
	}
}

?>
