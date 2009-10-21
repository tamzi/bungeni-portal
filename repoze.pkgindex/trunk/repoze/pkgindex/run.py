# publish a filesystem tree

def make_app(global_config, path=None):
    if path is None:
        raise ValueError('repoze.pkgindex requires a directory home')
    from repoze.bfg.router import make_app
    from repoze.pkgindex.models import Directory    
    def get_root(environ):
        return Directory(path)
    import repoze.pkgindex
    return make_app(get_root, repoze.pkgindex, options={
        'path': path})
