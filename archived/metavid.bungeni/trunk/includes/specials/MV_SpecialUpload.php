<?php

if (!defined('MEDIAWIKI')) die();
global $IP;
require_once( "$IP/includes/specials/SpecialUpload.php" );

function doSpecialUpload() {
	global $wgRequest;
	$form = new MV_SpecialUpload( $wgRequest );
	$form->execute();
}

SpecialPage::addPage( new SpecialPage('Mv_special_upload','',false,'doSpecialUpload',false) );

class MV_SpecialUpload extends UploadForm
{
//	function MV_SpecialUpload($wgRequest)
//	{
//	$this->wg = $wgRequest;
//		parent :: MV_SpecialUpload($wgRequest);
//	}
	function uploadWarning( $warning ) {
		global $wgOut;
		global $wgUseCopyrightUpload;

		$this->mSessionKey = $this->stashSession();
		if( !$this->mSessionKey ) {
			# Couldn't save file; an error has been displayed so let's go.
			return;
		}

		$wgOut->addHTML( Xml::element( 'h2', null, wfMsg( 'uploadwarning' ) ) . "\n" );
		$wgOut->addHTML( Xml::tags( 'ul', array( 'class' => 'warning' ), $warning ) . "\n" );

		$titleObj = SpecialPage::getTitleFor( 'Mv_special_upload' );

		if ( $wgUseCopyrightUpload ) {
			$copyright = Xml::hidden( 'wpUploadCopyStatus', $this->mCopyrightStatus ) . "\n" .
					Xml::hidden( 'wpUploadSource', $this->mCopyrightSource ) . "\n";
		} else {
			$copyright = '';
		}

		$wgOut->addHTML(
			Xml::openElement( 'form', array( 'method' => 'post', 'action' => $titleObj->getLocalURL( 'action=submit' ),
				 'enctype' => 'multipart/form-data', 'id' => 'uploadwarning' ) ) . "\n" .
			Xml::hidden( 'wpIgnoreWarning', '1' ) . "\n" .
			Xml::hidden( 'wpSessionKey', $this->mSessionKey ) . "\n" .
			Xml::hidden( 'wpUploadDescription', $this->mComment ) . "\n" .
			Xml::hidden( 'wpLicense', $this->mLicense ) . "\n" .
			Xml::hidden( 'wpDestFile', $this->mDesiredDestName ) . "\n" .
			Xml::hidden( 'wpWatchthis', $this->mWatchthis ) . "\n" .
			"{$copyright}<br />" .
			Xml::submitButton( wfMsg( 'ignorewarning' ), array ( 'name' => 'wpUpload', 'id' => 'wpUpload', 'checked' => 'checked' ) ) . ' ' .
			Xml::submitButton( wfMsg( 'reuploaddesc' ), array ( 'name' => 'wpReUpload', 'id' => 'wpReUpload' ) ) .
			Xml::closeElement( 'form' ) . "\n"
		);
	}
	
	function mainUploadForm( $msg='' ) {
		global $wgOut, $wgUser, $wgLang, $wgMaxUploadSize;
		global $wgUseCopyrightUpload, $wgUseAjax, $wgAjaxUploadDestCheck, $wgAjaxLicensePreview;
		global $wgRequest, $wgAllowCopyUploads;
		global $wgStylePath, $wgStyleVersion;

		$useAjaxDestCheck = $wgUseAjax && $wgAjaxUploadDestCheck;
		$useAjaxLicensePreview = $wgUseAjax && $wgAjaxLicensePreview;

		$adc = wfBoolToStr( $useAjaxDestCheck );
		$alp = wfBoolToStr( $useAjaxLicensePreview );
		$autofill = wfBoolToStr( $this->mDesiredDestName == '' );

		$wgOut->addScript( "<script type=\"text/javascript\">
wgAjaxUploadDestCheck = {$adc};
wgAjaxLicensePreview = {$alp};
wgUploadAutoFill = {$autofill};
</script>
<script type=\"text/javascript\" src=\"{$wgStylePath}/common/upload.js?{$wgStyleVersion}\"></script>
		" );

		if( !wfRunHooks( 'UploadForm:initial', array( &$this ) ) )
		{
			wfDebug( "Hook 'UploadForm:initial' broke output of the upload form" );
			return false;
		}

		if( $this->mDesiredDestName ) {
			$title = Title::makeTitleSafe( NS_IMAGE, $this->mDesiredDestName );
			// Show a subtitle link to deleted revisions (to sysops et al only)
			if( $title instanceof Title && ( $count = $title->isDeleted() ) > 0 && $wgUser->isAllowed( 'deletedhistory' ) ) {
				$link = wfMsgExt(
					$wgUser->isAllowed( 'delete' ) ? 'thisisdeleted' : 'viewdeleted',
					array( 'parse', 'replaceafter' ),
					$wgUser->getSkin()->makeKnownLinkObj(
						SpecialPage::getTitleFor( 'Undelete', $title->getPrefixedText() ),
						wfMsgExt( 'restorelink', array( 'parsemag', 'escape' ), $count )
					)
				);
				$wgOut->addHtml( "<div id=\"contentSub2\">{$link}</div>" );
			}

			// Show the relevant lines from deletion log (for still deleted files only)
			if( $title instanceof Title && $title->isDeleted() > 0 && !$title->exists() ) {
				$this->showDeletionLog( $wgOut, $title->getPrefixedText() );
			}
		}

		$cols = intval($wgUser->getOption( 'cols' ));

		if( $wgUser->getOption( 'editwidth' ) ) {
			$width = " style=\"width:100%\"";
		} else {
			$width = '';
		}

		if ( '' != $msg ) {
			$sub = wfMsgHtml( 'uploaderror' );
			$wgOut->addHTML( "<h2>{$sub}</h2>\n" .
			  "<span class='error'>{$msg}</span>\n" );
		}
		//$wgOut->addHTML( '<div id="uploadtext">' );
		//$wgOut->addWikiMsg( 'uploadtext', $this->mDesiredDestName );
		//$wgOut->addHTML( "</div>\n" );

		# Print a list of allowed file extensions, if so configured.  We ignore
		# MIME type here, it's incomprehensible to most people and too long.
		global $wgCheckFileExtensions, $wgStrictFileExtensions,
		$wgFileExtensions, $wgFileBlacklist;

		$allowedExtensions = '';
		if( $wgCheckFileExtensions ) {
			$delim = wfMsgExt( 'comma-separator', array( 'escapenoentities' ) );
			if( $wgStrictFileExtensions ) {
				# Everything not permitted is banned
				$extensionsList =
					'<div id="mw-upload-permitted">' .
					wfMsgWikiHtml( 'upload-permitted', implode( $wgFileExtensions, $delim ) ) .
					"</div>\n";
			} else {
				# We have to list both preferred and prohibited
				$extensionsList =
					'<div id="mw-upload-preferred">' .
					wfMsgWikiHtml( 'upload-preferred', implode( $wgFileExtensions, $delim ) ) .
					"</div>\n" .
					'<div id="mw-upload-prohibited">' .
					wfMsgWikiHtml( 'upload-prohibited', implode( $wgFileBlacklist, $delim ) ) .
					"</div>\n";
			}
		}

		# Get the maximum file size from php.ini as $wgMaxUploadSize works for uploads from URL via CURL only
		# See http://www.php.net/manual/en/ini.core.php#ini.upload-max-filesize for possible values of upload_max_filesize
		$val = trim( ini_get( 'upload_max_filesize' ) );
		$last = strtoupper( ( substr( $val, -1 ) ) );
		switch( $last ) {
			case 'G':
				$val2 = substr( $val, 0, -1 ) * 1024 * 1024 * 1024;
				break;
			case 'M':
				$val2 = substr( $val, 0, -1 ) * 1024 * 1024;
				break;
			case 'K':
				$val2 = substr( $val, 0, -1 ) * 1024;
				break;
			default:
				$val2 = $val;
		}
		$val2 = $wgAllowCopyUploads ? min( $wgMaxUploadSize, $val2 ) : $val2;
		$maxUploadSize = wfMsgExt( 'upload-maxfilesize', array( 'parseinline', 'escapenoentities' ), $wgLang->formatSize( $val2 ) );

		$sourcefilename = wfMsgExt( 'sourcefilename', 'escapenoentities' );
		$destfilename = wfMsgExt( 'destfilename', 'escapenoentities' );
		$summary = wfMsgExt( 'fileuploadsummary', 'parseinline' );

		$licenses = new Licenses();
		$license = wfMsgExt( 'license', array( 'parseinline' ) );
		$nolicense = wfMsgHtml( 'nolicense' );
		$licenseshtml = $licenses->getHtml();

		$ulb = wfMsgHtml( 'uploadbtn' );


		$titleObj = SpecialPage::getTitleFor( 'Mv_special_upload' );

		$encDestName = htmlspecialchars( $this->mDesiredDestName );

		$watchChecked = $this->watchCheck()
			? 'checked="checked"'
			: '';
		$warningChecked = $this->mIgnoreWarning ? 'checked' : '';

		// Prepare form for upload or upload/copy
		if( $wgAllowCopyUploads && $wgUser->isAllowed( 'upload_by_url' ) ) {
			$filename_form =
				"<input type='radio' id='wpSourceTypeFile' name='wpSourceType' value='file' " .
				   "onchange='toggle_element_activation(\"wpUploadFileURL\",\"wpUploadFile\")' checked='checked' />" .
				 "<input tabindex='1' type='file' name='wpUploadFile' id='wpUploadFile' " .
				   "onfocus='" .
				     "toggle_element_activation(\"wpUploadFileURL\",\"wpUploadFile\");" .
				     "toggle_element_check(\"wpSourceTypeFile\",\"wpSourceTypeURL\")' " .
				     "onchange='fillDestFilename(\"wpUploadFile\")' size='60' />" .
				wfMsgHTML( 'upload_source_file' ) . "<br/>" .
				"<input type='radio' id='wpSourceTypeURL' name='wpSourceType' value='web' " .
				  "onchange='toggle_element_activation(\"wpUploadFile\",\"wpUploadFileURL\")' />" .
				"<input tabindex='1' type='text' name='wpUploadFileURL' id='wpUploadFileURL' " .
				  "onfocus='" .
				    "toggle_element_activation(\"wpUploadFile\",\"wpUploadFileURL\");" .
				    "toggle_element_check(\"wpSourceTypeURL\",\"wpSourceTypeFile\")' " .
				    "onchange='fillDestFilename(\"wpUploadFileURL\")' size='60' disabled='disabled' />" .
				wfMsgHtml( 'upload_source_url' ) ;
		} else {
			$filename_form =
				"<input tabindex='1' type='file' name='wpUploadFile' id='wpUploadFile' " .
				($this->mDesiredDestName?"":"onchange='fillDestFilename(\"wpUploadFile\")' ") .
				"size='60' />" .
				"<input type='hidden' name='wpSourceType' value='file' />" ;
		}
		if ( $useAjaxDestCheck ) {
			$warningRow = "<tr><td colspan='2' id='wpDestFile-warning'>&nbsp;</td></tr>";
			$destOnkeyup = 'onkeyup="wgUploadWarningObj.keypress();"';
		} else {
			$warningRow = '';
			$destOnkeyup = '';
		}

		$encComment = htmlspecialchars( $this->mComment );

		$wgOut->addHTML(
			 Xml::openElement( 'form', array( 'method' => 'post', 'action' => $titleObj->getLocalURL(),
				 'enctype' => 'multipart/form-data', 'id' => 'mw-upload-form' ) ) .
			 Xml::openElement( 'fieldset' ) .
			 Xml::element( 'legend', null, wfMsg( 'upload' ) ) .
			 Xml::openElement( 'table', array( 'border' => '0', 'id' => 'mw-upload-table' ) ) .
			 "<tr>
			 	{$this->uploadFormTextTop}
				<td class='mw-label'>
					<label for='wpUploadFile'>{$sourcefilename}</label>
				</td>
				<td class='mw-input'>
					{$filename_form}
				</td>
			</tr>
			<tr>
				<td></td>
				<td>
					{$maxUploadSize}
					{$extensionsList}
				</td>
			</tr>
			<tr>
				<td class='mw-label'>
					<label for='wpDestFile'>{$destfilename}</label>
				</td>
				<td class='mw-input'>
					<input tabindex='2' type='text' name='wpDestFile' id='wpDestFile' size='60'
						value=\"{$encDestName}\" onchange='toggleFilenameFiller()' $destOnkeyup />
				</td>
			</tr>
			<tr>
				<td class='mw-label'>
					<label for='file_desc_msg'>stream desc msg</label>
				</td>
				<td class='mw-input'>
					<input tabindex='3' type='text' name='file_desc_msg' id='file_desc_msg' size='60'
						value=\"mv_ogg_low_quality\" />
				</td>
			</tr>
			<tr>
				<td class='mw-label'>
					<label for='wpUploadDescription'>{$summary}</label>
				</td>
				<td class='mw-input'>
					<textarea tabindex='4' name='wpUploadDescription' id='wpUploadDescription' rows='6'
						cols='{$cols}'{$width}>$encComment</textarea>
					{$this->uploadFormTextAfterSummary}
				</td>
			</tr>
			<tr>"
		);

		if ( $licenseshtml != '' ) {
			global $wgStylePath;
			$wgOut->addHTML( "
					<td class='mw-label'>
						<label for='wpLicense'>$license</label>
					</td>
					<td class='mw-input'>
						<select name='wpLicense' id='wpLicense' tabindex='4'
							onchange='licenseSelectorCheck()'>
							<option value=''>$nolicense</option>
							$licenseshtml
						</select>
					</td>
				</tr>
				<tr>"
			);
			if( $useAjaxLicensePreview ) {
				$wgOut->addHtml( "
						<td></td>
						<td id=\"mw-license-preview\"></td>
					</tr>
					<tr>"
				);
			}
		}

		if ( $wgUseCopyrightUpload ) {
			$filestatus = wfMsgExt( 'filestatus', 'escapenoentities' );
			$copystatus =  htmlspecialchars( $this->mCopyrightStatus );
			$filesource = wfMsgExt( 'filesource', 'escapenoentities' );
			$uploadsource = htmlspecialchars( $this->mCopyrightSource );

			$wgOut->addHTML( "
					<td class='mw-label' style='white-space: nowrap;'>
						<label for='wpUploadCopyStatus'>$filestatus</label></td>
					<td class='mw-input'>
						<input tabindex='5' type='text' name='wpUploadCopyStatus' id='wpUploadCopyStatus'
							value=\"$copystatus\" size='60' />
					</td>
				</tr>
				<tr>
					<td class='mw-label'>
						<label for='wpUploadCopyStatus'>$filesource</label>
					</td>
					<td class='mw-input'>
						<input tabindex='6' type='text' name='wpUploadSource' id='wpUploadCopyStatus'
							value=\"$uploadsource\" size='60' />
					</td>
				</tr>
				<tr>"
			);
		}

		$wgOut->addHtml( "
				<td></td>
				<td>
					<input tabindex='7' type='checkbox' name='wpWatchthis' id='wpWatchthis' $watchChecked value='true' />
					<label for='wpWatchthis'>" . wfMsgHtml( 'watchthisupload' ) . "</label>
					<input tabindex='8' type='checkbox' name='wpIgnoreWarning' id='wpIgnoreWarning' value='true' $warningChecked/>
					<label for='wpIgnoreWarning'>" . wfMsgHtml( 'ignorewarnings' ) . "</label>
				</td>
			</tr>
			$warningRow
			<tr>
				<td></td>
					<td class='mw-input'>
						<input tabindex='9' type='submit' name='wpUpload' value=\"{$ulb}\"" . $wgUser->getSkin()->tooltipAndAccesskey( 'upload' ) . " />
					</td>
			</tr>
			<tr>
				<td></td>
				<td class='mw-input'>"
		);
		//undesa
		$stream_id = $wgRequest->getVal('stream_id');
		$wgOut->addHTML("<input type=hidden name=stream_id value=$stream_id></input>");
		//undesa
		$wgOut->addWikiText( wfMsgForContent( 'edittools' ) );
		$wgOut->addHTML( "
				</td>
			</tr>" .
			Xml::closeElement( 'table' ) .
			Xml::hidden( 'wpDestFileWarningAck', '', array( 'id' => 'wpDestFileWarningAck' ) ) .
			Xml::closeElement( 'fieldset' ) .
			Xml::closeElement( 'form' )
		);
		$uploadfooter = wfMsgNoTrans( 'uploadfooter' );
		if( $uploadfooter != '-' && !wfEmptyMsg( 'uploadfooter', $uploadfooter ) ){
			$wgOut->addWikiText( Xml::tags( 'div',
				array( 'id' => 'mw-upload-footer-message' ), $uploadfooter ) );
		}
	}
	
	function processUpload(){
		global $wgUser, $wgOut, $wgFileExtensions,$wgScriptPath;
	 	
	 	$details = null;
	 	$value = null;
	 	global $mvMediaFilesTable, $mvStreamFilesTable, $wgRequest;
		$stream_id = $wgRequest->getVal('stream_id');
			
		$file_desc_msg =  $wgRequest->getVal('file_desc_msg');
		
		$newStream = MV_Stream::newStreamByID($stream_id);
		$files = $newStream->getFileList();			
 		$doAdd=true; 
 		foreach($files as $sf){
 				if($sf->file_desc_msg == $file_desc_msg){
 					$doAdd=false;
 				}
 		}
	 	if(!$doAdd)
	 	{
	 		$value = 99;
	 	}
	 	else
	 	{
	 		$value = $this->internalProcessUpload( $details );
	 	}
	 	
 			
		
		
		
	 	switch($value) {
			case self::SUCCESS:
				$html ='File has been uploaded successfully<br/>';
				$file = ''.$this->mLocalFile->getPath(); 
    			if (file_exists($file)) {
					$f = fopen($file,"rb");
					$header = fread($f, 512);
					$page['serial'] = substr($header, 14, 4);
					$page['segments'] = ord($header[26]);
				 	$page['rate'] = ord($header[27+$page['segments']+15]);
	  				$page['rate'] = ($page['rate'] << 8) | ord($header[27+$page['segments']+14]);
          			$page['rate'] = ($page['rate'] << 8) | ord($header[27+$page['segments']+13]);
          			$page['rate'] = ($page['rate'] << 8) | ord($header[27+$page['segments']+12]);
					fseek($f, -6000, SEEK_END);
					$end = fread($f, 6000);
					$tail = strstr($end, "OggS");
					if ($tail) {
		 				$serial = substr($tail, 14, 4);
	  					if ($serial == $page['serial']) {
	  						$duration = 103;
	    					$granulepos = ord($tail[6]);
	    					$granulepos = $granulepos | (ord($tail[7]) << 8);
	    					$granulepos = $granulepos | (ord($tail[8]) << 16);
	    					$granulepos = $granulepos | (ord($tail[9]) << 24);
	    					$granulepos = $granulepos | (ord($tail[10]) << 32);
	    					$granulepos = $granulepos | (ord($tail[11]) << 40);
	    					$granulepos = $granulepos | (ord($tail[12]) << 48);
	    					$granulepos = $granulepos | (ord($tail[13]) << 56);
	    					$duration = $granulepos/$page['rate'];
	  					}
					}
					fclose($f);
				}
				
				$dbr =& wfGetDB(DB_WRITE);
				$text = ''.$wgScriptPath.'/images/'.$this->mLocalFile->getUrlRel();
				
				if ($duration===null)$duration=0;
				if ($dbr->insert($mvMediaFilesTable,  array('path'=>$text,'duration'=>$duration,'file_desc_msg'=>$file_desc_msg), __METHOD__))
				{
					$result = $dbr->query("SELECT LAST_INSERT_ID() AS id");
					$row = $dbr->fetchObject($result);
					$id = $row->id;
					if ($dbr->insert($mvStreamFilesTable, array('file_id'=>$id,
						'stream_id'=>$stream_id
					), __METHOD__))
					{
						$stream_name = MV_Stream::getStreamNameFromId($stream_id);
						$title = Title::newFromText( $stream_name, MV_NS_STREAM  );
						$wgOut->redirect($title->getLocalURL("action=edit"));	
					}
					else {
						$html .= 'Inserting file path into DB failed, Please notify the Administrator immediately';
					}
				} else {
					$html .= 'Inserting file path into DB failed, Please notify the Administrator immediately';
				}
				
				/*
				
				if ($dbr->insert($mvStreamFilesTable, array('stream_id'=>$stream_id))) {
					$result = $dbr->query("SELECT LAST_INSERT_ID()");
					$row = $dbr->fetchObject($result);
					if ($duration===null)$duration=0;
					if ($dbr->insert($mvMediaFilesTable, array('id'=>$row->id,'path'=>$text,'duration'=>$duration))) {
					
						//$html .='<input type="button" name="Close" value="Close" Onclick="window.opener.document.getElementById(\'path\').value=\''.$wgScriptPath.'/images/'.$this->mLocalFile->getUrlRel().'\'; window.opener.document.getElementById(\'duration\').value='.floor($duration).'; window.close()"></input>' ;
						$stream_name = MV_Stream::getStreamNameFromId($stream_id);
						$title = Title::newFromText( $stream_name, MV_NS_STREAM  );
						$wgOut->redirect($title->getLocalURL("action=edit"));	
						
					}
					else {
						$html .= 'Inserting file path into DB failed, Please notify the Administrator immediately';
					}
				} else {
				$html .= 'Inserting file path into DB failed, Please notify the Administrator immediately';
				}
				
				
				*/
				
				$wgOut->addHTML($html);
				break;

			case self::BEFORE_PROCESSING:
				break;

			case self::LARGE_FILE_SERVER:
				$this->mainUploadForm( wfMsgHtml( 'largefileserver' ) );
				break;

			case self::EMPTY_FILE:
				$this->mainUploadForm( wfMsgHtml( 'emptyfile' ) );
				break;

			case self::MIN_LENGHT_PARTNAME:
				$this->mainUploadForm( wfMsgHtml( 'minlength1' ) );
				break;

			case self::ILLEGAL_FILENAME:
				$filtered = $details['filtered'];
				$this->uploadError( wfMsgWikiHtml( 'illegalfilename', htmlspecialchars( $filtered ) ) );
				break;

			case self::PROTECTED_PAGE:
				$this->uploadError( wfMsgWikiHtml( 'protectedpage' ) );
				break;

			case self::OVERWRITE_EXISTING_FILE:
				$errorText = $details['overwrite'];
				$overwrite = new WikiError( $wgOut->parse( $errorText ) );
				$this->uploadError( $overwrite->toString() );
				break;

			case self::FILETYPE_MISSING:
				$this->uploadError( wfMsgExt( 'filetype-missing', array ( 'parseinline' ) ) );
				break;

			case self::FILETYPE_BADTYPE:
				$finalExt = $details['finalExt'];
				$this->uploadError(
					wfMsgExt( 'filetype-banned-type',
						array( 'parseinline' ),
						htmlspecialchars( $finalExt ),
						implode(
							wfMsgExt( 'comma-separator', array( 'escapenoentities' ) ),
							$wgFileExtensions
						)
					)
				);
				break;

			case self::VERIFICATION_ERROR:
				$veri = $details['veri'];
				$this->uploadError( $veri->toString() );
				break;

			case self::UPLOAD_VERIFICATION_ERROR:
				$error = $details['error'];
				$this->uploadError( $error );
				break;

			case self::UPLOAD_WARNING:
				$warning = $details['warning'];
				$this->uploadWarning( $warning );
				break;

			case self::INTERNAL_ERROR:
				$internal = $details['internal'];
				$this->showError( $internal );
				break;
			case 99:
				$this->mainUploadForm('Type '.$file_desc_msg.' already exists');
				break;
			default:
				throw new MWException( __METHOD__ . ": Unknown value `{$value}`" );
	 	}
	}

}

?>
