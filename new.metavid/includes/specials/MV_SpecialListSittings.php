<?php

if ( !defined( 'MEDIAWIKI' ) ) die();

class MV_SpecialListSittings extends SpecialPage {

	protected $m_querystring = '';
	protected $m_params = array();
	protected $m_printouts = array();
	protected $m_editquery = false;
	var $mLimitsShown = array( 10, 25, 50, 100);
	/**
	 * Constructor
	 */
	public function __construct() {
		parent::__construct('Sittings');
	}

	function execute($p = '') {
		global $wgOut, $wgRequest, $smwgQEnabled, $smwgRSSEnabled, $wgUser;
		wfProfileIn('doSpecialAsk (SMW)');
		$skin = $wgUser->getSkin();
		if (!$smwgQEnabled) {
			$wgOut->addHTML('<br />' . wfMsg('smw_iq_disabled'));
		} else {
			if( $wgUser->isAllowed('add_sitting') ){
	$wgOut->addHTML('<div class="admin_links"><a href='.htmlspecialchars($skin->makeSpecialUrl("Add Sitting")).'>Add Sittings</a></div>');
			}
			$this->start_month = $wgRequest->getText('start_month');
			$this->start_year = $wgRequest->getVal('start_year');
			$this->end_month = $wgRequest->getText('end_month');
			$this->end_year = $wgRequest->getVal('end_year');
			$this->sitting_type=$wgRequest->getText('type');
			
			$this->getForm();
			$this->extractQueryParameters($p);
			
			$this->makeHTMLResult();
		}
		SMWOutputs::commitToOutputPage($wgOut); // make sure locally collected output data is pushed to the output!
		wfProfileOut('doSpecialAsk (SMW)');
	}


	
	protected function extractQueryParameters($p) {
		// This code rather hacky since there are many ways to call that special page, the most involved of
		// which is the way that this page calls itself when data is submitted via the form (since the shape
		// of the parameters then is governed by the UI structure, as opposed to being governed by reason).
		global $wgRequest, $wgOut;
		
		$query_string = '[[Stream:+]]';
		
		if (isset($this->start_month) && isset($this->start_year))
		{
			$start_q = ' [[Date Held::>'.$this->start_year.'/'.$this->start_month.'/01]]';
		}
		
		if (isset($start_q))
		{
			$query_string .= $start_q;
		}
		
		if (isset($this->end_month) && isset($this->end_year))
		{
			$end_q = ' [[Date Held::<'.$this->end_year.'/'.$this->end_month.'/31]]';
		}
		
		if (isset($end_q))
		{
			$query_string .= $end_q;
		}
		
		if (!($this->sitting_type == ''))
		{
			$type_q = ' [[Sitting Type::'.$this->sitting_type.']]';
		}
		
		if (isset($type_q))
		{
			$query_string .= $type_q;
		}
		
		//$wgOut->addHTML($query_string);
		$rawparams = SMWInfolink::decodeParameters($wgRequest->getVal( 'p' ), true);
		
		// Check for q= query string, used whenever this special page calls itself (via submit or plain link):
		$this->m_querystring = $query_string;
		if ($this->m_querystring != '') {
			$rawparams[] = $this->m_querystring;
		}
		// Check for param strings in po (printouts), appears in some links and in submits:
		$paramstring = "? Date_Held \n? Type";
		if ($paramstring != '') { // parameters from HTML input fields
			$ps = explode("\n", $paramstring); // params separated by newlines here (compatible with text-input for printouts)
			foreach ($ps as $param) { // add initial ? if omitted (all params considered as printouts)
				$param = trim($param);
				if ( ($param != '') && ($param{0} != '?') ) {
					$param = '?' . $param;
				}
				$rawparams[] = $param;
			}
		}

		// Now parse parameters and rebuilt the param strings for URLs
		SMWQueryProcessor::processFunctionParams($rawparams,$this->m_querystring,$this->m_params,$this->m_printouts);
		// Try to complete undefined parameter values from dedicated URL params
		if ( !array_key_exists('format',$this->m_params) ) {
			if (array_key_exists('rss', $this->m_params)) { // backwards compatibility (SMW<=1.1 used this)
				$this->m_params['format'] = 'rss';
			} else { // default
				$this->m_params['format'] = 'broadtable';
			}
		}
		$sortcount = $wgRequest->getVal( 'sc' );
		if (!is_numeric($sortcount)) {
			$sortcount = 0;
		}
		if ( !array_key_exists('order',$this->m_params) ) {
			$this->m_params['order'] = $wgRequest->getVal( 'order' ); // basic ordering parameter (, separated)
			for ($i=0; $i<$sortcount; $i++) {
				if ($this->m_params['order'] != '') {
					$this->m_params['order'] .= ',';
				}
				$value = $wgRequest->getVal( 'order' . $i );
				$value = ($value == '')?'ASC':$value;
				$this->m_params['order'] .= $value;
			}
		}
		if ( !array_key_exists('sort',$this->m_params) ) {
			$this->m_params['sort'] = $wgRequest->getText( 'sort' ); // basic sorting parameter (, separated)
			for ($i=0; $i<$sortcount; $i++) {
				if ( ($this->m_params['sort'] != '') || ($i>0) ) { // admit empty sort strings here
					$this->m_params['sort'] .= ',';
				}
				$this->m_params['sort'] .= $wgRequest->getText( 'sort' . $i );
			}
		}
		// Find implicit ordering for RSS -- needed for downwards compatibility with SMW <=1.1
		if ( ($this->m_params['format'] == 'rss') && ($this->m_params['sort'] == '') && ($sortcount==0)) {
			foreach ($this->m_printouts as $printout) {
				if ((strtolower($printout->getLabel()) == "date") && ($printout->getTypeID() == "_dat")) {
					$this->m_params['sort'] = $printout->getTitle()->getText();
					$this->m_params['order'] = 'DESC';
				}
			}
		}
		if ( !array_key_exists('offset',$this->m_params) ) {
			$this->m_params['offset'] = $wgRequest->getVal( 'offset' );
			if ($this->m_params['offset'] == '')  $this->m_params['offset'] = 0;
		}
		if ( !array_key_exists('limit',$this->m_params) ) {
			$this->m_params['limit'] = $wgRequest->getVal( 'limit' );
			if ($this->m_params['limit'] == '') {
				 $this->m_params['limit'] = ($this->m_params['format'] == 'rss')?10:20; // standard limit for RSS
			}
		}

		$this->m_editquery = ( $wgRequest->getVal( 'eq' ) != '' ) || ('' == $this->m_querystring );
	}

	protected function makeHTMLResult() {
		global $wgOut;
		$result = '';
		$result_mime = false; // output in MW Special page as usual

		// build parameter strings for URLs, based on current settings
		$urltail = '&q=' . urlencode($this->m_querystring);

		$tmp_parray = array();
		foreach ($this->m_params as $key => $value) {
			if ( !in_array($key,array('sort', 'order', 'limit', 'offset', 'title')) ) {
				$tmp_parray[$key] = $value;
			}
		}
		$urltail .= '&p=' . urlencode(SMWInfolink::encodeParameters($tmp_parray));
		$printoutstring = '';
		foreach ($this->m_printouts as $printout) {
			$printoutstring .= $printout->getSerialisation() . "\n";
		}
		if ('' != $printoutstring)          $urltail .= '&po=' . urlencode($printoutstring);
		if ('' != $this->m_params['sort'])  $urltail .= '&sort=' . $this->m_params['sort'];
		if ('' != $this->m_params['order']) $urltail .= '&order=' . $this->m_params['order'];

		if ($this->m_querystring != '') {
			$queryobj = SMWQueryProcessor::createQuery($this->m_querystring, $this->m_params, false, '', $this->m_printouts);
			$queryobj->querymode = SMWQuery::MODE_INSTANCES; ///TODO: Somewhat hacky (just as the query mode computation in SMWQueryProcessor::createQuery!)
			$res = smwfGetStore()->getQueryResult($queryobj);
			// try to be smart for rss/ical if no description/title is given and we have a concept query:
			if ($this->m_params['format'] == 'rss') {
				$desckey = 'rssdescription';
				$titlekey = 'rsstitle';
			} elseif ($this->m_params['format'] == 'icalendar') {
				$desckey = 'icalendardescription';
				$titlekey = 'icalendartitle';
			} else { $desckey = false; }
			if ( ($desckey) && ($queryobj->getDescription() instanceof SMWConceptDescription) &&
			     (!isset($this->m_params[$desckey]) || !isset($this->m_params[$titlekey])) ) {
				$concept = $queryobj->getDescription()->getConcept();
				if ( !isset($this->m_params[$titlekey]) ) {
					$this->m_params[$titlekey] = $concept->getText();
				}
				if ( !isset($this->m_params[$desckey]) ) {
					$dv = end(smwfGetStore()->getSpecialValues($concept, SMW_SP_CONCEPT_DESC));
					if ($dv instanceof SMWConceptValue) {
						$this->m_params[$desckey] = $dv->getDocu();
					}
				}
			}
			$printer = SMWQueryProcessor::getResultPrinter($this->m_params['format'], SMWQueryProcessor::SPECIAL_PAGE, $res);
			$result_mime = $printer->getMimeType($res);
			if ($result_mime == false) {
				if ($res->getCount() > 0) {
					$navigation = $this->getNavigationBar($res, $urltail);
					$result = '<div style="text-align: center;">';
					$result .= '</div>' . $printer->getResult($res, $this->m_params,SMW_OUTPUT_HTML);
					$result .= '<div style="text-align: center;">' . $navigation . '</div>';
				} else {
					$result = '<div style="text-align: center;">' . wfMsg('smw_result_noresults') . '</div>';
				}
			} else { // make a stand-alone file
				$result = $printer->getResult($res, $this->m_params,SMW_OUTPUT_FILE);
				$result_name = $printer->getFileName($res); // only fetch that after initialising the parameters
			}
		}

		if ($result_mime == false) {
				$wgOut->setPageTitle('Sittings');
			
			$wgOut->addHTML($result);
		} else {
			$wgOut->disable();
			header( "Content-type: $result_mime; charset=UTF-8" );
			if ($result_name !== false) {
				header( "Content-Disposition: attachment; filename=$result_name");
			}
			print $result;
		}
	}

	protected function getNavigationBar($res, $urltail) {
		global $wgUser, $smwgQMaxLimit;
		$skin = $wgUser->getSkin();
		$offset = $this->m_params['offset'];
		$limit  = $this->m_params['limit'];
		// prepare navigation bar
		if ($offset > 0) {
			$navigation = '<a href="' . htmlspecialchars($skin->makeSpecialUrl('Sittings','offset=' . max(0,$offset-$limit) . '&limit=' . $limit . $urltail)) . '">' . wfMsg('smw_result_prev') . '</a>';
		} else {
			$navigation = wfMsg('smw_result_prev');
		}

		$navigation .= '&nbsp;&nbsp;&nbsp;&nbsp; <b>' . wfMsg('smw_result_results') . ' ' . ($offset+1) . '&ndash; ' . ($offset + $res->getCount()) . '</b>&nbsp;&nbsp;&nbsp;&nbsp;';

		if ($res->hasFurtherResults()) 
			$navigation .= ' <a href="' . htmlspecialchars($skin->makeSpecialUrl('Sittings','offset=' . ($offset+$limit) . '&limit=' . $limit . $urltail)) . '">' . wfMsg('smw_result_next') . '</a>';
		else $navigation .= wfMsg('smw_result_next');

		$max = false; $first=true;
		foreach (array(20,50,100,250,500) as $l) {
			if ($max) continue;
			if ($first) {
				$navigation .= '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(';
				$first = false;
			} else $navigation .= ' | ';
			if ($l > $smwgQMaxLimit) {
				$l = $smwgQMaxLimit;
				$max = true;
			}
			if ( $limit != $l ) {
				$navigation .= '<a href="' . htmlspecialchars($skin->makeSpecialUrl('Sittings','offset=' . $offset . '&limit=' . $l . $urltail)) . '">' . $l . '</a>';
			} else {
				$navigation .= '<b>' . $l . '</b>';
			}
		}
		$navigation .= ')';
		return $navigation;
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
	
	function getLimitSelect() {
        	global $wgLang;
        	$s = "<select name=\"limit\">";
         	foreach ( $this->mLimitsShown as $limit ) {
             		$selected = $limit == $this->mLimit ? 'selected="selected"' : '';
            		$formattedLimit = $wgLang->formatNum( $limit );
            		$s .= "<option value=\"$limit\" $selected>$formattedLimit</option>\n";
         	}
        	$s .= "</select>";
         	return $s;
	}
 


	function getForm() {
		global $wgRequest, $wgMiserMode, $wgOut;
		
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
			//$this->getHiddenFields( array( 'limit', 'end_month', 'end_year', 'start_month', 'start_year', 'type' ) ) .
			Xml::closeElement( 'fieldset' ) .
			Xml::closeElement( 'form' ) . "\n";
		$wgOut->addHTML($s);
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
			if (!is_null($this->sitting_type) && ($this->sitting_type == $row->name))
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
	
	
	
}?>
