<?php

if (!defined('MEDIAWIKI')) die();

global $IP;

class MV_Status {

	var $action='';
	var $article='';
	
	public function __construct($action, $article) {
		$this->action = $action;
		$this->article = $article;
	}

	public function display() {
		global $wgOut;
		//$text = "Hello World";
		//$this->doEdit($text,"Status");
		//$article->doRedirect();
		//$wgOut->addHTML($text);
		//wfRunHooks('ArticleSaveComplete', array(&$this, &$wgUser));
		$this->execute();
		//$this->test();
	}
	
	function test()
	{
		$querystring = 'Status::Incomplete';
		
		SMWQueryProcessor::getResultFromQueryString ($querystring, $params, $extraprintouts, $outputmode, true); 		
	}
	/*
	public function execute($query = '') {
		global $wgRequest, $wgOut, $wgUser, $smwgQMaxInlineLimit, $smwgIP;
		
		require_once( "$smwgIP/includes/storage/SMW_Store.php" );
		$skin = $wgUser->getSkin();

		// get the GET parameters
		//$attributestring = $wgRequest->getVal( 'property' );
		//$valuestring = $wgRequest->getVal( 'value' );
		//$params = SMWInfolink::decodeParameters($query, false);
		//reset($params);
		// no GET parameters? Then try the URL
		//if ($attributestring == '') $attributestring = current($params);
		//if ($valuestring == '') $valuestring = next($params);
		
		$attributestring = 'Status';
		$valuestring = $this->action;
		
		$user = $this->article->getTitle();
		
		
		$attribute = Title::newFromText( $attributestring, SMW_NS_PROPERTY );
		
		if (NULL === $attribute) { $attributestring = ''; } else { $attributestring = $attribute->getText(); }

		$limit = $wgRequest->getVal( 'limit' );
		if ('' == $limit) $limit =  20;
		$offset = $wgRequest->getVal( 'offset' );
		if ('' == $offset) $offset = 0;
		$html = '';
		
		//$spectitle = Title::makeTitle( 2, $this->article->getTitle() );

		if ('' == $attributestring) { // empty page. If no attribute given the value does not matter
			$html .= wfMsg('smw_sbv_docu') . "\n";
		} else {
			global $smwgIP;
			include_once($smwgIP . '/includes/SMW_DataValueFactory.php');
			// Now that we have an attribute, let's figure out the datavalue
			$value = SMWDataValueFactory::newPropertyObjectValue( $attribute, $valuestring );
			if ( $value->isValid() == FALSE ) { // no value understood
				$html .= wfMSG('smw_sbv_novalue', $skin->makeLinkObj($attribute, $attribute->getText()));
				$valuestring = '';
			} else { // everything is given
				
				
				$wgOut->setPagetitle( $attribute->getText() . ' ' . $value->getShortHTMLText(NULL) );
				$valuestring = $value->getWikiValue();

				$options = new SMWRequestOptions();
				$options->limit = $limit+1;
				$options->offset = $offset;
				
				//$descriptions = new array();
				//$descriptions[0] = new 
				//$conjunction = new SMWConjunction ($descriptions);
				
				$querystring = 'Status::Incomplete';
				
				$query = new SMWQuery();
				$query->setQueryString($querystring);
				$query->setDescription();
				
				//$res = &smwfGetStore()->getPropertySubjects( $attribute, $value, $options );
				$res = &smwfGetStore()->getQueryResult($query);
				$count = count($res);


				$html .= wfMsg('smw_sbv_displayresult', $skin->makeLinkObj($attribute, $attribute->getText()), $value->getShortHTMLText($skin)) . "<br />\n";

				// prepare navigation bar
				if ($offset > 0)
					$navigation = '<a href="' . htmlspecialchars($skin->makeSpecialUrl('SearchByProperty','offset=' . max(0,$offset-$limit) . '&limit=' . $limit . '&property=' . urlencode($attribute->getText()) .'&value=' . urlencode($value->getWikiValue()))) . '">' . wfMsg('smw_result_prev') . '</a>';
				else
					$navigation = wfMsg('smw_result_prev');

				$navigation .= '&nbsp;&nbsp;&nbsp;&nbsp; <b>' . wfMsg('smw_result_results') . ' ' . ($offset+1) . '&ndash; ' . ($offset + min($count, $limit)) . '</b>&nbsp;&nbsp;&nbsp;&nbsp;';

				if ($count>$limit) {
					$navigation .= ' <a href="' . htmlspecialchars($skin->makeSpecialUrl('SearchByProperty', 'offset=' . ($offset+$limit) . '&limit=' . $limit . '&property=' . urlencode($attribute->getText()) . '&value=' . urlencode($value->getWikiValue())))  . '">' . wfMsg('smw_result_next') . '</a>';
				} else {
					$navigation .= wfMsg('smw_result_next');
				}

				$max = false; $first=true;
				foreach (array(20,50,100,250,500) as $l) {
					if ($max) continue;
					if ($first) {
						$navigation .= '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(';
						$first = false;
					} else
						$navigation .= ' | ';
					if ($l > $smwgQMaxInlineLimit) {
						$l = $smwgQMaxInlineLimit;
						$max = true;
					}
					if ( $limit != $l ) {
						$navigation .= '<a href="' . htmlspecialchars($skin->makeSpecialUrl('SearchByProperty','offset=' . $offset . '&limit=' . $l . '&property=' . urlencode($attribute->getText()) . '&value=' . urlencode($value->getWikiValue()))) . '">' . $l . '</a>';
					} else {
						$navigation .= '<b>' . $l . '</b>';
					}
				}
				$navigation .= ')';

				if ($count == 0) {
					$html .= wfMsg( 'smw_result_noresults' );
				} else { // if there are plenty of results anyway
					global $smwgIP;
					// no need to show the navigation bars when there is not enough to navigate
					if (($offset>0) || ($count>$limit)) $html .= '<br />' . $navigation;
					$html .= "<ul>\n";
					foreach ($res as $t) {
						$browselink = SMWInfolink::newBrowsingLink('+',$t->getPrefixedText());
						$html .= '<li>' . $skin->makeKnownLinkObj($t) . '&nbsp;&nbsp;' . $browselink->getHTML($skin) . "</li> \n";
					}
					$html .= "</ul>\n";
					if (($offset>0) || ($count>$limit)) $html .= $navigation;
				}
			}
		}
		$wgOut->addHTML($html);
		
	}
	*/
	function execute()
	{
		global $wgRequest, $wgOut, $wgUser, $smwgQMaxInlineLimit,$smwgIP;
		$skin = $wgUser->getSkin();
		$limit = $wgRequest->getVal( 'limit' );
		if ('' == $limit) $limit =  20;
		$offset = $wgRequest->getVal( 'offset' );
		if ('' == $offset) $offset = 0;
		$html = '';
		
		$attributestring = 'Status';
		$action = $this->action;
		
		$userPageTitle = $this->article->getTitle();
		$user_nick = $userPageTitle->getDBkey();
		
		$user = User::newFromName($user_nick);
		
		$groups = $user->getGroups();
		include_once( "$smwgIP/includes/SMW_QueryProcessor.php" );
		$query = '[[Status::'.$action.']]';
		if (in_array('reporter', $groups))
			$query .= ' [[Reported By::'.$user->getRealName().']]';
		if (in_array('reader', $groups))
			$query .= ' [[Read By::'.$user->getRealName().']]';
		if (in_array('editor', $groups))
			$query .= ' [[Edited By::'.$user->getRealName().']]';
		
		$params = array('offset' => $offset, 'limit' => $limit, 'format' => 'broadtable', 'mainlabel' => ' ', 'link' => 'all', 'default' => wfMsg('smw_result_noresults'), 'sort' => $sort, 'order' => $order);
		$queryobj = SMWQueryProcessor::createQuery($query, $params, false);
		$res = smwfGetStore()->getQueryResult($queryobj);
		$printer = new SMWTableResultPrinter('broadtable',false);
		$result = $printer->getResultHTML($res, $params);
		// prepare navigation bar
		if ($offset > 0) 
			$navigation = '<a href="' . htmlspecialchars($skin->makeUrl("$userPageTitle",'action='.$action.'&offset=' . max(0,$offset-$limit) . '&limit=' . $limit  . '&sort=' . urlencode($sort) .'&order=' . urlencode($order))) . '">' . wfMsg('smw_result_prev') . '</a>';
		else $navigation = wfMsg('smw_result_prev');

		$navigation .= '&nbsp;&nbsp;&nbsp;&nbsp; <b>' . wfMsg('smw_result_results') . ' ' . ($offset+1) . '&ndash; ' . ($offset + $res->getCount()) . '</b>&nbsp;&nbsp;&nbsp;&nbsp;';

		if ($res->hasFurtherResults()) 
			$navigation .= ' <a href="' . htmlspecialchars($skin->makeUrl("$userPageTitle",'action='.$action.'&offset=' . ($offset+$limit) . '&limit=' . $limit . '&sort=' . urlencode($sort) .'&order=' . urlencode($order))) . '">' . wfMsg('smw_result_next') . '</a>';
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
				$navigation .= '<a href="' . htmlspecialchars($skin->makeSpecialUrl('Ask','offset=' . $offset . '&limit=' . $l . '&query=' . urlencode($query) . '&sort=' . urlencode($sort) .'&order=' . urlencode($order))) . '">' . $l . '</a>';
			} else {
					$navigation .= '<b>' . $l . '</b>';
			}
		}
		$navigation .= ')';

		$html .= '<br /><div style="text-align: center;">' . $navigation;
		$html .= '<br />' . $result;
		$html .= '<br />' . $navigation . '</div>';
		$wgOut->addHTML($html);
	}
}
