<?php

if ( !defined( 'MEDIAWIKI' ) ) die();

class MV_SpecialAddMP extends SpecialPage {
	public function __construct() {
		parent::__construct('Add_MP');
	}

	function execute() {
		global $wgOut, $wgRequest, $wgUser;
		
		if( $wgUser->isAllowed('add_mp') ){
			$this->first_name = htmlspecialchars($wgRequest->getText('first_name'));
			$this->surname = htmlspecialchars($wgRequest->getText('surname'));
			$this->middle_name = htmlspecialchars($wgRequest->getText('middle_name'));
			$this->constituency = htmlspecialchars($wgRequest->getText('constituency'));
			$this->bio = htmlspecialchars($wgRequest->getText('bio'));
			$wgOut->addHTML($this->processForm());
			$wgOut->addHTML($this->getForm());
		}
		else
		{
			$wgOut->addHTML('<div class="errorbox">You DO NOT have permission to add a Member of Parliament</div>');
		}
		
		$wgOut->setPageTitle('Add Member of Parliament');
	}
	
	function processForm()
	{
		global $wgRequest;
		$posted = $wgRequest->wasPosted();
		if ($posted)
		{
			$error = false;
			$s = '<ul>';
			if ('' == $this->first_name){
				$error = true;
				$s .= '<li>First Name</li>';
			}
			if ('' == $this->surname){
				$error = true;
				$s .= '<li>Surname</li>';
			}
			if ('' == $this->constituency){
				$error = true;
				$s .= '<li>Constituency</li>';
			}
			$s .= '</ul>';
			if ($error)
			{
				return '<div class="errorbox">Fill in the following Fields'.$s.'</div> <br/>';
			}
			else
			{
				if ('' != trim($this->middle_name))
					$fullname = $this->first_name.'_'.$this->middle_name.'_'.$this->surname;
				else
					$fullname = $this->first_name.'_'.$this->surname;
					
				$title = Title::newFromText( $fullname, MV_NS_MEMBER_OF_PARLIAMENT );
				$article = new Article( $title );
				
				$text = $this->bio . "[[Constituency::".$this->constituency." | ]] ";
				
				if ($article->exists())
				{
					return '<div class="errorbox">An MP with the same name already exists</div>';
				}
				else
				{
					$article->doEdit($text, 'Member of Parliament');
					$article->doRedirect();
					
				}
			}
		}
	} 
	
	function getForm(){
		global $wgRequest;
		$s = Xml::openElement('div', array('class'=>'addMP'));
		$s .= '<table name="add_MP_table" width=90%>';
		$s .= '<tr><td>';
		$s .=  Xml::openElement('form', array( 'method' => 'post', 'action' => $this->getTitle()->getLocalURL(), 'id' => 'Add-MP-form' ));
		$s .= Xml::openElement('label', array('name'=>'lbl_first_name'));
		$s .= 'First Name';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		$s .= Xml::input('first_name', 30, $this->first_name);
		$s .= '</td></tr>';
		$s .= '<tr><td>';
		$s .= Xml::openElement('label', array('name'=>'lbl_surname'));
		$s .= 'Surname ';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		$s .= Xml::input('surname', 30, $this->surname);
		$s .= '</td></tr>';
		$s .= '<tr><td>';
		$s .= Xml::openElement('label', array('name'=>'lbl_middle_name'));
		$s .= 'Middle Name or Initial ';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		$s .= Xml::input('Middle_name', 30, $this->middle_name);
		$s .= '</td></tr>';
		$s .= '<tr><td>';
		$s .= Xml::openElement('label', array('name'=>'lbl_constituency'));
		$s .= 'Constituency ';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		$s .= Xml::input('constituency', 30, $this->constituency);
		$s .= '</td></tr>';
		$s .= '<tr><td>'; 
		$s .= Xml::openElement('label', array('name'=>'Bio'));
		$s .= 'Bio ';
		$s .= Xml::closeElement('label');
		$s .= '</td><td>';
		$s .= Xml::textarea('bio', $this->bio, 40, 5);
		$s .= '</td><tr>';
		$s .= '<tr><td colspan = 2>';
		$s .= Xml::submitButton('Add MP');
		$s .= '</td></tr>';
		$s .= Xml::closeElement('form');
		$s .= '</table>';
		$s .= Xml::closeElement('div');
		return $s;
	}
}
