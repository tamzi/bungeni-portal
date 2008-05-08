<?php

/*
 * Created on Jul 26, 2007
 *
 * All Metavid Wiki code is Released Under the GPL2
 * for more info visit http:/metavid.ucsc.edu/code
 * 
 * ovewrites the existing special search to add in metavid specific features
 */
if (!defined('MEDIAWIKI'))
	die();

global $IP, $smwgIP;
//require_once($smwgIP . '/includes/SMW_Storage.php');
//require_once ("$IP/includes/SpecialPage.php");
//require_once ("$IP/includes/Title.php");
//require_once ("$IP/includes/QueryPage.php");

function doSpecialSearch($par = null) {
	//list( $limit, $offset ) = wfCheckLimits();
	$MvSpecialSearch = new MvSearch();
	$MvSpecialSearch->doSearchPage();
}
//metavid search page (only search video media)
SpecialPage :: addPage(new SpecialPage('MvMediaSearch', '', true, 'doSpecialSearch', false));

//todo hook into mediaWiki special search page to inject media results
/*
 * simple/quick implementation ... 
 * future version should be better integrated with semantic wiki and or 
 * an external search engine of some sort
 * 
 * exmple get request: filter 0, type match, value = wars 
 * ?f[0]['t']=m&f[0]['v']=wars
 */
class MvSearch {
	var $filter_types = array (
		'match',
		'spoken_by',
		'category',
		//'smw_property' not active yet
	);
	var $filter_match_andor = array (
		'AND' => 'contains',
		'OR' => 'may contain',
		'NOT' => 'doesn\'t contain'
	);	
	function doSearchPage() {
		global $wgRequest, $wgOut;

		//add nessesary js to wgOut: 
		mvfAddHTMLHeader('search');
		//add the search placeholder 
		$wgOut->addHTML($this->dynamicSearchControl());
		$this->doSearch();
		$wgOut->addHTML($this->getHTMLResults());
	}
	function dynamicSearchControl() {
		$title = SpecialPage :: getTitleFor('MvMediaSearch');
		$action = $title->escapeLocalURL();

		return "\n<form id=\"mv_media_search\" method=\"get\" " .
		"action=\"$action\">\n{$this->list_active_filters()}\n</form>\n";
	}
	function doSearch() {
		global $mvgIP;
		require_once ($mvgIP . '/includes/MV_Index.php');
		$this->results = MvIndex :: doFiltersQuery($this->filters);
	}
	function getHTMLResults() {
		global $mvgIP, $wgOut, $mvgScriptPath, $mvgContLang, $wgUser, $wgParser;
		//print_r($this->results);
		//for each stream range:
		$o = '';
		//print_r($this->results );
		require_once ($mvgIP . '/includes/MV_Title.php');
		require_once ($mvgIP . '/includes/MV_MetavidInterface/MV_Overlay.php');
		if (count($this->results) == 0) {
			return '<h3>' . wfMsg('mv_search_no_results') . '</h3>';
		}
		foreach ($this->results as $stream_id => & $stream_set) {
			$matches = 0;
			$stream_out = $mvTitle = '';
			$sk = & $wgUser->getSkin();
			foreach ($stream_set as & $srange) {
				$cat_html = $mvd_out = '';
				$range_match=0;
				foreach ($srange['rows'] as & $mvd) {					
					$matches++;
					if (isset ($mvd->text)) {
						//@@todo parse category info if present
						//$cat_html = $mvd->text;					
						//run via parser to add in Category info: 
						$parserOptions = ParserOptions :: newFromUser($wgUser);
						$parserOptions->setEditSection(false);
						$parserOptions->setTidy(true);
						$title = Title :: MakeTitle(MV_NS_MVD, $mvd->wiki_title);
						$parserOutput = $wgParser->parse($mvd->text, $title, $parserOptions);
						$cats = $parserOutput->getCategories();
						foreach ($cats as $catkey => $title_str) {
							$title = Title :: MakeTitle(NS_CATEGORY, $catkey);
							$cat_html .= ' ' . $sk->makeKnownLinkObj($title, $catkey);
						}
						//add category pre-text:
						if ($cat_html != '')
							$cat_html = wfMsg('Categories') . ':' . $cat_html;

						//$wgOut->addCategoryLinks( $parserOutput->getCategories() );						
						//$cat_html = $sk->getCategories();
						//empty out the categories
						//$wgOut->mCategoryLinks = array();	
					}
					$mvTitle = new MvTitle($mvd->wiki_title);

					//retive only the first article: 
					//$title = Title::MakeTitle(MV_NS_MVD, $mvd->wiki_title);
					//$article = new Article($title);
					$bgcolor=MV_Overlay::getMvdBgColor($mvd);

					$mvd_out .= '<span style="background:#'.$bgcolor.'">&nbsp; &nbsp; &nbsp; &nbsp;' . $mvTitle->getTimeDesc() . '&nbsp;</span>';
					$mvd_out .= '<a title="' . wfMsg('mv_expand_play') . '" href="javascript:mv_ex(\'' . $mvd->id . '\')"><img id="mv_img_ex_'.$mvd->id.'" border="0" src="' . $mvgScriptPath . '/skins/images/closed.png"></a>' .
					'&nbsp;';
					//output control liniks:
					//make stream title link: 
					$mvStreamTitle = Title :: MakeTitle(MV_NS_STREAM, $mvTitle->getNearStreamName());
					//$mvTitle->getStreamName() .'/'.$mvTitle->getStartTime() .'/'. $mvTitle->getEndTime() );
					$mvd_out .= $sk->makeKnownLinkObj($mvStreamTitle, '<img border="0" src="' . $mvgScriptPath . '/skins/images/run_mv_stream.png">', '', '', '', '', ' title="' . wfMsg('mv_view_in_stream_interface') . '" ');
										
					//$title = MakeTitle::()
					$mvd_out .='&nbsp;';
					$mvdTitle = Title::MakeTitle(MV_NS_MVD, $mvd->wiki_title);
					$mvd_out .= $sk->makeKnownLinkObj($mvdTitle, '<img border="0" src="' . $mvgScriptPath . '/skins/images/run_mediawiki.png">', '', '', '', '', ' title="' . wfMsg('mv_view_wiki_page') . '" ');
								
					$mvd_out .= '<div id="mvr_' . $mvd->id . '" style="display:none;background:#'.$bgcolor.';" ></div>';

					$mvd_out .= '<br>' . "\n";
				}
				if(count($srange['rows'])!=1){					
					$stream_out .= '&nbsp;' . $cat_html . ' In range:' . 
					seconds2ntp($srange['s']) . ' to ' . seconds2ntp($srange['e']) .
					wfMsg('mv_match_text', count($srange['rows'])).'<br>' . "\n";
					$stream_out .= $mvd_out;
				}else{								
					$stream_out .= $mvd_out;
				}
			}
			$nsary = $mvgContLang->getNamespaceArray();
			//output stream name and mach count
			/*$o.='<br><img class="mv_stream_play_button" name="'.$nsary[MV_NS_STREAM].':' .
				$mvTitle->getStreamName() .
					'" align="left" src="'.$mvgScriptPath.'/skins/mv_embed/images/vid_play_sm.png">';
			*/
			$o .= '<h3>' . $mvTitle->getStreamNameText() . wfMsg('mv_match_text', $matches).'</h3>';
			$o .= '<div id="mv_stream_' . $stream_id . '">' . $stream_out . '</div>';
		}
		return $o;
	}
	function hr_nav_matches_in_rage($stream_range_set) {

	}
	//output expanded request with retired title text
	function expand_wt($mvd_id) {
		global $wgOut,$mvgIP;
		global $mvDefaultSearchVideoPlaybackRes;
		require_once($mvgIP.'/includes/MV_Index.php');
		require_once($mvgIP.'/includes/MV_Title.php');
		require_once($mvgIP.'/includes/MV_MetavidInterface/MV_Overlay.php');
		
		$mvd = MvIndex::getMVDbyId($mvd_id);
		if(count($mvd)!=0){			
			$mvTitle = new MvTitle($mvd->wiki_title);
			//validate title and load stream ref:
			if($mvTitle->validRequestTitle()){
				list($vWidth, $vHeight) = explode('x', $mvDefaultSearchVideoPlaybackRes); 
				$embedHTML='<span style="float:left;width:'.($vWidth+20).'px">' . 
									$mvTitle->getEmbedVideoHtml($mvd_id, $mvDefaultSearchVideoPlaybackRes) .
							'</span>';
				$wgOut->clearHTML();
								
				$title = Title::MakeTitle(MV_NS_MVD,$mvd->wiki_title);
				$article = new Article($title);
				$MvOverlay = new MV_Overlay();				
				$MvOverlay->parse_format_text( $article->getContent(), $mvTitle);
				$bgcolor = $MvOverlay->getMvdBgColor($mvd);
				$pageHTML = $wgOut->getHTML();
				//encasulate page html: 
				$pageHTML='<span style="padding-top:10px;float:left;width:450px">'.$pageHTML.'</span>';						
				return $embedHTML. $pageHTML. '<div style="clear: both;"/>';
			}else{
				return wfMsg('mvBadMVDtitle');
			}
		}else{
			return wfMsg('mv_error_mvd_not_found');
		}
		//$title = Title::MakeTitle(MV_NS_MVD, $wiki_title);
		//$article = new Article($title);
		//output table with embed left, and content right
		//return $wgOut->parse($article->getContent());
	}
	function list_active_filters() {
		global $mvgScriptPath;
		if (isset ($_GET['f'])) {
			//@@todo some input proccessing
			$this->filters = $_GET['f'];
		} else {
			$this->filters = array (
				array (
					't' => 'match',
					'v' => ''
				)
			);
		}
		$s = '<div id="mv_active_filters" style="height:60px;">';
		$s .= print_r($this->filters, true) . '<br>';
		foreach ($this->filters as $i => $filter) {
			if (!isset ($filter['v']))
				$filter['v'] = '';
			if (!isset ($filter['t']))
				$filter['t'] = '';
			//output the master selecter per line: 
			$s .= '<span id="mvs_' . $i . '">';
			$s .= $this->selector($i, 't', $filter['t']);
			$s .= '<span id="mvs_' . $i . '_tc">';
			switch ($filter['t']) {
				case 'match' :
					$s .= $this->text_entry($i, 'v', $filter['v'], ' mv_hl_text');
					break;
				case 'category' :
					//$s.=$this->get_ref_ac($i, $filter['v']);
					$s .= $this->text_entry($i, 'v', $filter['v']);
					break;
				case 'spoken_by' :
					$s .= $this->get_ref_person($i, $filter['v'], true);
					break;
				case 'smw_property' :

				break;
			}
			$s .= '</span>';
			if ($i > 0)
				$s .= '&nbsp; <a href="javascript:mv_remove_filter(' .
				$i . ');">' .
				'<img title="' . wfMsg('mv_remove_filter') . '" ' .
				'src="' . $mvgScriptPath . '/skins/images/cog_delete.png"></a>';
			$s .= '</span>';
		}
		$s .= '</div>';
		//refrence remove 
		$s .= '<a id="mv_ref_remove" style="display:none;" ' .
		'href="">' .
		'<img title="' . wfMsg('mv_remove_filter') . '" ' .
		'src="' . $mvgScriptPath . '/skins/images/cog_delete.png"></a>';

		//ref missing person image ref: 							
		$s .= $this->get_ref_person();

		//add link:
		$s .= '<a href="javascript:mv_add_filter();">' .
		'<img border="0" title="' . wfMsg('mv_add_filter') . '" ' .
		'src="' . $mvgScriptPath . '/skins/images/cog_add.png"></a><br>';

		$s .= '<input id="mv_do_search" type="submit" ' .
		' value="' . wfMsg('mv_run_search') . '">';
		return $s;
	}
	function get_ref_person($inx = '', $person_name = MV_MISSING_PERSON_IMG, $disp = false) {
		if ($disp) {
			$tname = 'f[' . $inx . '][v]';
			$inx = '_' . $inx;
			$disp = 'inline';
		} else {
			$tname = '';
			$inx = '';
			$person_name = '';
			$disp = 'none';
		}
		//make the missing person image ref: 
		$imgTitle = Title :: makeTitle(NS_IMAGE, $person_name . '.jpg');
		if (!$imgTitle->exists()) {
			$imgTitle = Title :: makeTitle(NS_IMAGE, MV_MISSING_PERSON_IMG);
		}

		$img = wfFindFile($imgTitle);
		if (!$img) {
			$img = wfLocalFile($imgTitle);
		}
		//print "title is: " .$imgTitle->getDBKey() ."IMAGE IS: " . $img->getURL();

		return '<span class="mv_person_ac" id="mv_person' . $inx . '" style="display:' . $disp . ';width:90px;">' .
		'<img id="mv_person_img' . $inx . '" style="padding:2px;" src="' . $img->getURL() . '" width="44">' .
		'<input id="mv_person_input' . $inx . '" class="mv_search_text" style="font-size: 12px;" size="9" ' .
		'type="text" name="' . $tname . '" value="' . $person_name . '" autocomplete="off">' .
		'<div id="mv_person_choices' . $inx . '" class="autocomplete"></div>' .
		'</span>';
	}
	function selector($i, $key, $selected = '') {
		$s= '<select id="mv_sel_' . $i . '" class="mv_search_select" style="font-size: 12px;" name="f[' . $i . '][' . $key . ']" >' . "\n";
		if ($key == 't')
			$items = $this->filter_types;
		$sel = ($selected == '') ? 'selected' : '';
		$s .= '<option value="na" ' . $sel . '>' . wfMsg('mv_search_sel_' . $key) . '</option>' . "\n";
		foreach ($items as $item) {
			$sel = ($selected == $item) ? $sel = 'selected' : '';
			$s .= '<option value="' . $item . '" ' . $sel . '>' . wfMsg('mv_search_' . $item) . '</option>' . "\n";
		}
		$s .= '</select>';
		return $s;
	}
	//could be a sugest: 
	function text_entry($i, $key, $val = '', $more_class='') {
		$s = '<input class="mv_search_text'.$more_class.'" style="font-size: 12px;" onchange="" 
						size="9" type="text" name="f[' . $i . '][' . $key . ']" value="' . $val . '">';
		return $s;
	}
}
?>
