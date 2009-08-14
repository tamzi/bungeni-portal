registry = dict(version='8.3.2.1')
def bind():
	from cPickle import loads as _loads
	_lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
	_marker = _loads('ccopy_reg\n_reconstructor\np1\n(cchameleon.core.generation\nMarker\np2\nc__builtin__\nobject\np3\nNtRp4\n.')
	_init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
	_re_amp = _loads("csre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
	_translate = _loads('cchameleon.core.generation\nfast_translate\np1\n.')
	_lookup_name = _loads('cchameleon.core.codegen\nlookup_name\np1\n.')
	_init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
	_init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
	_init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
	_path = _loads('ccopy_reg\n_reconstructor\np1\n(cfive.pt.expressions\nFiveTraverser\np2\nc__builtin__\nobject\np3\nNtRp4\n.')
	def render(econtext, rcontext=None):
		macros = econtext.get('macros')
		_slots = econtext.get('_slots')
		target_language = econtext.get('target_language')
		u'_init_stream()'
		(_out, _write) = _init_stream()
		u'_init_tal()'
		(_attributes, repeat) = _init_tal()
		u'_init_default()'
		_default = _init_default()
		u'None'
		default = None
		u'None'
		_domain = None
		_tmp_domain0 = _domain
		u"u'plone'"
		_domain = u'plone'
		u"%(translate)s(u'heading_personal_tools', domain=%(domain)s, mapping=None, target_language=%(language)s, default=u'Personal tools')"
		_write(u'<div id="portal-personaltools-wrapper">\n\n<h5 class="hiddenStructure">')
		_result = _translate(u'heading_personal_tools', domain=_domain, mapping=None, target_language=target_language, default=u'Personal tools')
		u'_result'
		_tmp1 = _result
		u'view.user_actions or not view.anonymous'
		_write((_tmp1 + u'</h5>\n\n'))
		_tmp1 = (_lookup_attr(econtext['view'], 'user_actions') or not (_lookup_attr(econtext['view'], 'anonymous')))
		if _tmp1:
			pass
			u'view/subcontext'
			_write(u'<ul id="portal-personaltools" class="visualInline">\n\n        ')
			_tmp1 = _path(econtext['view'], econtext['request'], True, 'subcontext')
			if _tmp1:
				pass
				u'view/subcontext'
				_write(u'')
				_tmp1 = _path(econtext['view'], econtext['request'], True, 'subcontext')
				item = None
				(_tmp1, _tmp2) = repeat.insert('item', _tmp1)
				for item in _tmp1:
					_tmp2 = (_tmp2 - 1)
					u"''"
					_write(u'<li class="navigation">\n            ')
					_default.value = default = ''
					u'item/title'
					_content = _path(item, econtext['request'], True, 'title')
					u'item/url'
					_write(u'<a')
					_tmp3 = _path(item, econtext['request'], True, 'url')
					if _tmp3 is _default:
						_tmp3 = None
					if (_tmp3 is None or _tmp3 is False):
						pass
					else:
						if not (isinstance(_tmp3, unicode)):
							_tmp3 = str(_tmp3)
						if '&' in _tmp3:
							if ';' in _tmp3:
								_tmp3 = _re_amp.sub('&amp;', _tmp3)
							else:
								_tmp3 = _tmp3.replace('&', '&amp;')
						if '<' in _tmp3:
							_tmp3 = _tmp3.replace('<', '&lt;')
						if '>' in _tmp3:
							_tmp3 = _tmp3.replace('>', '&gt;')
						if '"' in _tmp3:
							_tmp3 = _tmp3.replace('"', '&quot;')
						_write((' href="' + _tmp3) + '"')
					u'_content'
					_write('>')
					_tmp3 = _content
					_tmp = _tmp3
					if (_tmp.__class__ not in (str, unicode, int, float) and hasattr(_tmp, '__html__')):
						_write(_tmp.__html__())
					elif _tmp is not None:
						if not (isinstance(_tmp, unicode)):
							_tmp = str(_tmp)
						if '&' in _tmp:
							if ';' in _tmp:
								_tmp = _re_amp.sub('&amp;', _tmp)
							else:
								_tmp = _tmp.replace('&', '&amp;')
						if '<' in _tmp:
							_tmp = _tmp.replace('<', '&lt;')
						if '>' in _tmp:
							_tmp = _tmp.replace('>', '&gt;')
						_write(_tmp)
					_write(u'</a>\n          </li>')
					if _tmp2 == 0:
						break
					_write(' ')
				_write(u'\n        ')
			u"not(_path(view, request, True, 'anonymous'))"
			_write(u'\n        \n')
			_tmp1 = not (_path(econtext['view'], econtext['request'], True, 'anonymous'))
			if _tmp1:
				pass
				u'view/homelink_url'
				_write(u'<li><a id="user-name"')
				_tmp1 = _path(econtext['view'], econtext['request'], True, 'homelink_url')
				if _tmp1 is _default:
					_tmp1 = None
				if (_tmp1 is None or _tmp1 is False):
					pass
				else:
					if not (isinstance(_tmp1, unicode)):
						_tmp1 = str(_tmp1)
					if '&' in _tmp1:
						if ';' in _tmp1:
							_tmp1 = _re_amp.sub('&amp;', _tmp1)
						else:
							_tmp1 = _tmp1.replace('&', '&amp;')
					if '<' in _tmp1:
						_tmp1 = _tmp1.replace('<', '&lt;')
					if '>' in _tmp1:
						_tmp1 = _tmp1.replace('>', '&gt;')
					if '"' in _tmp1:
						_tmp1 = _tmp1.replace('"', '&quot;')
					_write((' href="' + _tmp1) + '"')
				u"''"
				_write('>')
				_default.value = default = ''
				u'here/user.gif'
				_content = _path(econtext['here'], econtext['request'], True, 'user.gif')
				u'_content'
				_tmp1 = _content
				_tmp = _tmp1
				if (_tmp.__class__ not in (str, unicode, int, float) and hasattr(_tmp, '__html__')):
					_write(_tmp.__html__())
				elif _tmp is not None:
					if not (isinstance(_tmp, unicode)):
						_tmp = str(_tmp)
					_write(_tmp)
				u"u'\\n                John\\n           '"
				_write(u'\n            ')
				_default.value = default = u'\n                John\n           '
				u'view/user_name'
				_content = _path(econtext['view'], econtext['request'], True, 'user_name')
				u'_content'
				_write(u'<span class="visualCaseSensitive">')
				_tmp1 = _content
				_tmp = _tmp1
				if (_tmp.__class__ not in (str, unicode, int, float) and hasattr(_tmp, '__html__')):
					_write(_tmp.__html__())
				elif _tmp is not None:
					if not (isinstance(_tmp, unicode)):
						_tmp = str(_tmp)
					if '&' in _tmp:
						if ';' in _tmp:
							_tmp = _re_amp.sub('&amp;', _tmp)
						else:
							_tmp = _tmp.replace('&', '&amp;')
					if '<' in _tmp:
						_tmp = _tmp.replace('<', '&lt;')
					if '>' in _tmp:
						_tmp = _tmp.replace('>', '&gt;')
					_write(_tmp)
				_write(u'</span></a></li>\n   ')
			u'view/user_actions'
			_write(u'\n\n')
			_tmp1 = _path(econtext['view'], econtext['request'], True, 'user_actions')
			action = None
			(_tmp1, _tmp2) = repeat.insert('action', _tmp1)
			for action in _tmp1:
				_tmp2 = (_tmp2 - 1)
				_write(u'')
				try:
					u'action/icon '
					icon = _path(action, econtext['request'], True, 'icon')
				except Exception, e:
					u' nothing'
					icon = None
				u"icon is not None and icon or view.getIconFor(action['category'], action['id'], None)"
				icon = ((icon is not None and icon) or _lookup_attr(econtext['view'], 'getIconFor')(action['category'], action['id'], None))
				u'visualIcon actionicon-${action/category}-${action/id}'
				class_name = ('%s%s%s%s' % (u'visualIcon actionicon-', _path(action, econtext['request'], True, 'category'), u'-', _path(action, econtext['request'], True, 'id')))
				u'icon is not None and class_name or nothing'
				class_name = ((icon is not None and class_name) or econtext['nothing'])
				u'class_name'
				_write(u'<li')
				_tmp3 = _path(class_name, econtext['request'], True)
				if _tmp3 is _default:
					_tmp3 = None
				if (_tmp3 is None or _tmp3 is False):
					pass
				else:
					if not (isinstance(_tmp3, unicode)):
						_tmp3 = str(_tmp3)
					if '&' in _tmp3:
						if ';' in _tmp3:
							_tmp3 = _re_amp.sub('&amp;', _tmp3)
						else:
							_tmp3 = _tmp3.replace('&', '&amp;')
					if '<' in _tmp3:
						_tmp3 = _tmp3.replace('<', '&lt;')
					if '>' in _tmp3:
						_tmp3 = _tmp3.replace('>', '&gt;')
					if '"' in _tmp3:
						_tmp3 = _tmp3.replace('"', '&quot;')
					_write((' class="' + _tmp3) + '"')
				u'action/url'
				_write(u'>\n            <a')
				_tmp3 = _path(action, econtext['request'], True, 'url')
				if _tmp3 is _default:
					_tmp3 = u''
				if (_tmp3 is None or _tmp3 is False):
					pass
				else:
					if not (isinstance(_tmp3, unicode)):
						_tmp3 = str(_tmp3)
					if '&' in _tmp3:
						if ';' in _tmp3:
							_tmp3 = _re_amp.sub('&amp;', _tmp3)
						else:
							_tmp3 = _tmp3.replace('&', '&amp;')
					if '<' in _tmp3:
						_tmp3 = _tmp3.replace('<', '&lt;')
					if '>' in _tmp3:
						_tmp3 = _tmp3.replace('>', '&gt;')
					if '"' in _tmp3:
						_tmp3 = _tmp3.replace('"', '&quot;')
					_write((' href="' + _tmp3) + '"')
				u"icon is not None and 'visualIconPadding' or nothing"
				_tmp3 = ((icon is not None and 'visualIconPadding') or econtext['nothing'])
				if _tmp3 is _default:
					_tmp3 = None
				if (_tmp3 is None or _tmp3 is False):
					pass
				else:
					if not (isinstance(_tmp3, unicode)):
						_tmp3 = str(_tmp3)
					if '&' in _tmp3:
						if ';' in _tmp3:
							_tmp3 = _re_amp.sub('&amp;', _tmp3)
						else:
							_tmp3 = _tmp3.replace('&', '&amp;')
					if '<' in _tmp3:
						_tmp3 = _tmp3.replace('<', '&lt;')
					if '>' in _tmp3:
						_tmp3 = _tmp3.replace('>', '&gt;')
					if '"' in _tmp3:
						_tmp3 = _tmp3.replace('"', '&quot;')
					_write((' class="' + _tmp3) + '"')
				u'action/title'
				_write('>')
				_content = _path(action, econtext['request'], True, 'title')
				u'_content'
				_tmp = _content
				u'%(translate)s(_tmp, domain=%(domain)s, mapping=None, target_language=%(language)s, default=None)'
				_tmp3 = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
				_tmp = _tmp3
				if (_tmp.__class__ not in (str, unicode, int, float) and hasattr(_tmp, '__html__')):
					_write(_tmp.__html__())
				elif _tmp is not None:
					if not (isinstance(_tmp, unicode)):
						_tmp = str(_tmp)
					_write(_tmp)
				_write(u'</a>\n        </li>\n    ')
				if _tmp2 == 0:
					break
				_write(' ')
			_write(u'\n\n</ul>')
		_write(u'\n</div>')
		_domain = _tmp_domain0
		return _out.getvalue()
	return render

registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
