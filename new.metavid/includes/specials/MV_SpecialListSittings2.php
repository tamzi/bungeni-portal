<?php

if ( !defined( 'MEDIAWIKI' ) ) die();

class MV_SpecialListSittings extends SpecialPage {

	public function __construct() {
		
		parent::__construct( 'Sittings' );
	}

	function execute() {
		global $wgOut;
		$pager = new MV_SpecialQuerySittings;
		$limit = $pager->getForm();
		$body = $pager->getBody();
		$nav = $pager->getNavigationBar();
		$wgOut->setPageTitle('Sittings');
		$wgOut->addHTML( "$limit<br />\n$body<br />\n$nav" );
	}
}


class MV_SpecialQuerySittings extends TablePager {
	var $mFieldNames = null;
	var $mQueryConds = array();
	var $mLimitsShown = array( 10, 25, 50, 100);
	var $type='';

	function __construct() {
		global $wgRequest, $wgMiserMode;
		if ( $wgRequest->getText( 'sort', 'date' ) == 'date' ) {
			$this->mDefaultDirection = true;
		} else {
			$this->mDefaultDirection = false;
		}
/*		
		$search = $wgRequest->getText( 'ilsearch' );
		if ( $search != '' && !$wgMiserMode ) {
			$nt = Title::newFromUrl( $search );
			if( $nt ) {
				$dbr = wfGetDB( DB_SLAVE );
				$m = $dbr->strencode( strtolower( $nt->getDBkey() ) );
				$m = str_replace( "%", "\\%", $m );
				$m = str_replace( "_", "\\_", $m );
				$this->mQueryConds = array( "LOWER(img_name) LIKE '%{$m}%'" );
			}
		}
*/
		$start_month = $wgRequest->getText('start_month');
		$start_year = $wgRequest->getVal('start_year');
		$end_month = $wgRequest->getText('end_month');
		$end_year = $wgRequest->getVal('end_year');
		$this->type=$wgRequest->getText('type');
		$query='';
		$other_conds = false;
		if (isset($start_month) && isset($start_year) && isset($end_month) && isset($end_year))
		{
			$query .="date >= \"".htmlspecialchars($start_year)."-".htmlspecialchars($start_month)."-00\" and date <= \"".htmlspecialchars($end_year)."-".htmlspecialchars($end_month)."-30\"";
			$other_conds = true;
			$this->mQueryConds = array($query);
		}
		if ($this->type != "")
		{
			if ($other_conds)
				$query .= ' and ';
			$query.= "type=\"".htmlspecialchars($this->type)."\"";
		$this->mQueryConds = array($query);	
		}
		parent::__construct();
	}

	function getFieldNames() {
		if ( !$this->mFieldNames ) {
			$this->mFieldNames = array(
				'name' => 'Name',
				'type' => 'Sitting Type',
				'date' => 'Date Held',
				'duration' => 'Duration'
			);
		}
		return $this->mFieldNames;
	}

	function isFieldSortable( $field ) {
		static $sortable = array('date', 'type', 'name', 'duration' );
		return in_array( $field, $sortable );
	}

	function getQueryInfo() {
		global $wgRequest;
		$fields = $this->getFieldNames();
		$fields = array_keys( $fields );
		
		
		
		return array(
			'tables' => 'sittings',
			'fields' => $fields,
			'conds' => $this->mQueryConds
		);
	}

	function getDefaultSort() {
		return 'date';
	}

	function getStartBody() {
		# Do a link batch query for user pages
/*		
		if ( $this->mResult->numRows() ) {
			$lb = new LinkBatch;
			$this->mResult->seek( 0 );
			while ( $row = $this->mResult->fetchObject() ) {
				if ( $row->img_user ) {
					$lb->add( NS_USER, str_replace( ' ', '_', $row->img_user_text ) );
				}
			}
			$lb->execute();
		}
*/
		return parent::getStartBody();
	}

	function formatValue( $field, $value ) {
		global $wgLang;
		switch ( $field ) {
			case 'date':
				return date( 'jS F Y', strtotime($value));
			case 'name':
				$text = htmlspecialchars( $value );
				return $text;
			case 'type':
				$text = htmlspecialchars( $value );
				return $text;
			case 'duration':
				$text = htmlspecialchars( seconds2ntp($value) );
				return $text;
		}
	}
	function monthSelector( $selected = '', $name = 'month' ) {
         	global $wgLang;
         	$options = array();
         	if( is_null( $selected ) )
             		$selected = '';
         	for( $i = 1; $i < 13; $i++ )
                 	$options[] = Xml::option( $wgLang->getMonthName( $i ), $i, $selected == $i );
        	return Xml::openElement( 'select', array('name' => $name ) )
            	 . implode( "\n", $options )
             	. Xml::closeElement( 'select' );
     	}

	function getForm() {
		global $wgRequest, $wgMiserMode;
		
		global $mv_start_year;
		$s = Xml::openElement( 'form', array( 'method' => 'get', 'action' => $this->getTitle()->getLocalURL(), 'id' => 'sitting-form' ) ) .
			Xml::openElement( 'fieldset' ) .
			Xml::element( 'legend', null, 'Filter Sittings' ) ;
		$s.= Xml::openElement('label', array('name'=>'monthselector'));
		$s.= 'Held between ';
		$start_month = (is_numeric($wgRequest->getVal('start_month'))) ? htmlspecialchars($wgRequest->getVal('start_month')) : 1; 
		$s .= $this->monthSelector($start_month,'start_month'); 
		$start_year = (is_numeric($wgRequest->getVal('start_year'))) ? htmlspecialchars($wgRequest->getVal('start_year')) : $mv_start_year;
		$s .= $this->getYears('start_year', $start_year);
		$s .= ' and ';
		$today = getdate();
		$end_month = (is_numeric($wgRequest->getVal('end_month'))) ? htmlspecialchars($wgRequest->getVal('end_month')) : $today[mon];
		$s .= $this->monthSelector($end_month,'end_month');
		$end_year = (is_numeric($wgRequest->getVal('end_year'))) ? htmlspecialchars($wgRequest->getVal('end_year')) : $today[year];
		$s .= $this->getYears('end_year', $end_year);
		$s .= Xml::closeElement('label');
		$s .= Xml::openElement('label', array('name'=>'type'));
		$s .= ' of Type ';
		$s .= $this->typeSelector(); 
		$s .= Xml::closeElement('label');
		//$s .= '<br/>';
		
		$s .= ' '. Xml::tags( 'label', null, wfMsgHtml( 'table_pager_limit', $this->getLimitSelect() ) );

		$s .= ' ' .
			Xml::submitButton( wfMsg( 'table_pager_limit_submit' ) ) ."\n" .
			$this->getHiddenFields( array( 'limit', 'end_month', 'end_year', 'start_month', 'start_year', 'type' ) ) .
			Xml::closeElement( 'fieldset' ) .
			Xml::closeElement( 'form' ) . "\n";
		return $s;
	}
	
	function typeSelector()
	{
		$dbr = wfGetDB(DB_SLAVE); 
		
		$result = $dbr->select($dbr->tablename('sitting_types'), '*');
		$s = '';
		$s .= Xml::openElement('select', array('name'=>'type'));
		$s .=Xml::option("all","");
		while ($row = $dbr->fetchObject($result))
		{
			if (!is_null($this->type) && ($this->type == $row->name))
			{
				$s.=Xml::option($row->name,$row->name, true);
			}
			else
			{
				$s.=Xml::option($row->name,$row->name);
			}	
		}
		$s .= Xml::closeElement('select');
		return $s;
	}

	function getYears($name, $yearSelected = null)
	{
		global $mv_start_year;
		$start_year = $mv_start_year;
		$today = getdate();
		$year = $today[year];
		//$list = array();
		$str = Xml::openElement('select',array('name'=>$name));;
		while ($start_year <= $year)
		{
			if (isset($yearSelected) && ($yearSelected == $start_year))
			{
				$str .= Xml::tags('option', array('value'=>$start_year, 'selected'=>'true'), $start_year);
			}
			else
				$str .= Xml::tags('option', array('value'=>$start_year), $start_year);
			$start_year++;
		}  
		$str .= Xml::closeElement('select');
		return $str;
	}
	
	
	function getTableClass() {
		return 'wikitable sitting ' . parent::getTableClass();
	}

	function getNavClass() {
		return 'sittinglist_nav ' . parent::getNavClass();
	}

	function getSortHeaderClass() {
		return 'sortheader ' . parent::getSortHeaderClass();
	}
}
