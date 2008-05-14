<?php

if (!defined('MEDIAWIKI')) die();
global $IP;
require_once( "$IP/includes/SpecialUpload.php" );

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
		$wgOut->addHTML( '<div id="uploadtext">' );
		$wgOut->addWikiMsg( 'uploadtext', $this->mDesiredDestName );
		$wgOut->addHTML( "</div>\n" );

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
					<label for='wpUploadDescription'>{$summary}</label>
				</td>
				<td class='mw-input'>
					<textarea tabindex='3' name='wpUploadDescription' id='wpUploadDescription' rows='6'
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
		global $wgUser, $wgOut, $wgFileExtensions;
	 	$details = null;
	 	$value = null;
	 	$value = $this->internalProcessUpload( $details );

	 	switch($value) {
			case self::SUCCESS:
				$html ='File has been uploaded successfully<br/>';
				$html .='<input type="button" name="Close" value="Close" Onclick="window.opener.document.getElementById(\'path\').value=\''.$this->mLocalFile->getPath().'\'; window.close()"></input>' ;
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

			default:
				throw new MWException( __METHOD__ . ": Unknown value `{$value}`" );
	 	}
	}

}

?>
