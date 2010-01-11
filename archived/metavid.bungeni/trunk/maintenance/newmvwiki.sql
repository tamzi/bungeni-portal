-- phpMyAdmin SQL Dump
-- version 2.11.3deb1ubuntu1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 18, 2008 at 02:37 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.4-2ubuntu5.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `newmvwiki`
--

-- --------------------------------------------------------

--
-- Table structure for table `logging`
--

CREATE TABLE IF NOT EXISTS `logging` (
  `log_type` varbinary(10) NOT NULL default '',
  `log_action` varbinary(10) NOT NULL default '',
  `log_timestamp` binary(14) NOT NULL default '19700101000000',
  `log_user` int(10) unsigned NOT NULL default '0',
  `log_namespace` int(11) NOT NULL default '0',
  `log_title` varchar(255) character set latin1 collate latin1_bin NOT NULL default '',
  `log_comment` varchar(255) NOT NULL default '',
  `log_params` blob NOT NULL,
  `log_id` int(10) unsigned NOT NULL auto_increment,
  `log_deleted` tinyint(3) unsigned NOT NULL default '0',
  PRIMARY KEY  (`log_id`),
  KEY `type_time` (`log_type`,`log_timestamp`),
  KEY `user_time` (`log_user`,`log_timestamp`),
  KEY `page_time` (`log_namespace`,`log_title`,`log_timestamp`),
  KEY `times` (`log_timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2694 ;

-- --------------------------------------------------------

--
-- Table structure for table `mv_category`
--

CREATE TABLE IF NOT EXISTS `mv_category` (
  `id` int(11) NOT NULL auto_increment,
  `title` varchar(30) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

-- --------------------------------------------------------

--
-- Table structure for table `mv_media_files`
--

CREATE TABLE IF NOT EXISTS `mv_media_files` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `base_offset` int(10) NOT NULL default '0',
  `duration` int(9) NOT NULL,
  `path_type` enum('mvprime','cap1','ext_cspan','ext_archive_org','ext_url') character set utf8 collate utf8_unicode_ci NOT NULL,
  `file_desc_msg` varchar(255) character set utf8 collate utf8_unicode_ci NOT NULL,
  `path` text character set utf8 collate utf8_unicode_ci NOT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='base urls for path types are hard coded' AUTO_INCREMENT=129 ;

-- --------------------------------------------------------

--
-- Table structure for table `mv_mvd_index`
--

CREATE TABLE IF NOT EXISTS `mv_mvd_index` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `mv_page_id` int(10) unsigned NOT NULL,
  `wiki_title` varchar(100) collate utf8_unicode_ci NOT NULL,
  `mvd_type` varchar(32) collate utf8_unicode_ci NOT NULL,
  `stream_id` int(11) NOT NULL,
  `start_time` int(7) unsigned NOT NULL,
  `end_time` int(7) unsigned default NULL,
  `text` text collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `wiki_title` (`wiki_title`),
  KEY `mvd_type` (`mvd_type`),
  KEY `stream_id` (`stream_id`),
  KEY `stream_time_start` (`start_time`,`end_time`),
  FULLTEXT KEY `text` (`text`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='metavid data index' AUTO_INCREMENT=6365 ;

-- --------------------------------------------------------

--
-- Table structure for table `mv_sittings`
--

CREATE TABLE IF NOT EXISTS `mv_sittings` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) NOT NULL,
  `start_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_date` date NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=128 ;

-- --------------------------------------------------------

--
-- Table structure for table `mv_streams`
--

CREATE TABLE IF NOT EXISTS `mv_streams` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(48) collate utf8_unicode_ci NOT NULL,
  `state` enum('available','available_more_otw','live','otw','failed') collate utf8_unicode_ci default NULL,
  `date_start_time` int(10) default NULL,
  `duration` int(7) default NULL,
  `sitting_id` int(11) NOT NULL,
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `adj_start_time` (`date_start_time`),
  KEY `state` (`state`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=91 ;

-- --------------------------------------------------------

--
-- Table structure for table `mv_stream_files`
--

CREATE TABLE IF NOT EXISTS `mv_stream_files` (
  `stream_id` int(11) NOT NULL,
  `file_id` int(11) NOT NULL,
  PRIMARY KEY  (`stream_id`,`file_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `mv_stream_images`
--

CREATE TABLE IF NOT EXISTS `mv_stream_images` (
  `id` int(11) NOT NULL auto_increment,
  `stream_id` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `stream_id` (`stream_id`,`time`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 COMMENT='time to images table' AUTO_INCREMENT=1222 ;

-- --------------------------------------------------------

--
-- Table structure for table `mv_url_cache`
--

CREATE TABLE IF NOT EXISTS `mv_url_cache` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `url` varchar(255) NOT NULL,
  `post_vars` text,
  `req_time` int(11) NOT NULL,
  `result` text,
  UNIQUE KEY `id` (`id`),
  KEY `url` (`url`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 COMMENT='simple url cache (as to not tax external services too much) ' AUTO_INCREMENT=10 ;

-- --------------------------------------------------------

--
-- Table structure for table `sitting_assignment`
--

CREATE TABLE IF NOT EXISTS `sitting_assignment` (
  `sitting_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`sitting_id`,`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sitting_types`
--

CREATE TABLE IF NOT EXISTS `sitting_types` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `type` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;
